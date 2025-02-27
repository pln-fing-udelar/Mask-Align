#!/usr/bin/env python
# Copyright 2021-Present The THUAlign Authors
import argparse
import os
import socket
import time

import torch
import torch.distributed as dist

import thualign.data as data
import thualign.models as models
import thualign.utils as utils
import thualign.utils.alignment as alignment_utils


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate alignments neural alignment models",
        usage="infer_fast.py [<args>] [-h | --help]"
    )
    # test args
    parser.add_argument("--alignment-output", help="path to save generated alignments")

    # configure file
    parser.add_argument("--config", required=True, help="Provided config file")
    parser.add_argument("--base-config", help="base config file")
    parser.add_argument("--data-config", help="data config file")
    parser.add_argument("--model-config", help="base config file")
    parser.add_argument("--exp", "-e", default='DEFAULT', help="name of experiments")

    return parser.parse_args()


def load_vocabulary(params):
    params.vocabulary = {
        "source": data.Vocabulary(params.vocab[0]),
        "target": data.Vocabulary(params.vocab[1])
    }
    return params


def to_cuda(features):
    for key in features:
        features[key] = features[key].cuda()

    return features


def get_first_greater_than(l, threshold):
    for idx, val in enumerate(l):
        if val > threshold:
            return idx
    return -1


def get_last_greater_than(l, threshold):
    last_idx = -1
    for idx, val in enumerate(l):
        if val > threshold:
            last_idx = idx
    return last_idx


def get_answer_token_indexes(ans_idxs, tokens):
    idx1 = -1
    idx2 = -1
    current_char = 0
    search1 = True

    char_idx1, char_idx2 = int(ans_idxs[0].split(":")[0]), int(ans_idxs[0].split(":")[1])

    for idx, tok in enumerate(tokens):
        current_char += len(tok) + 1
        if char_idx1 < current_char and search1:
            idx1 = idx
            search1 = False
        if char_idx2 < current_char:
            idx2 = idx
            break

    return idx1, idx2 + 1


def gen_align(params):
    """Generate alignments"""
    with socket.socket() as s:
        s.bind(("localhost", 0))
        port = s.getsockname()[1]
        url = "tcp://localhost:" + str(port)
    dist.init_process_group("nccl", init_method=url, rank=0, world_size=1)

    params = load_vocabulary(params)
    checkpoint = getattr(params, "checkpoint", None) or utils.best_checkpoint(params.output)

    torch.set_default_tensor_type(torch.cuda.FloatTensor)

    if params.half:
        torch.set_default_dtype(torch.half)
        torch.set_default_tensor_type(torch.cuda.HalfTensor)

    # Create model
    with torch.no_grad():
        model = models.get_model(params).cuda()

        if params.half:
            model = model.half()

        model.eval()
        print(f'loading checkpoint: {checkpoint}')
        state = torch.load(checkpoint, map_location="cpu")
        model.load_state_dict(state["model"])

        get_infer_dataset = data.AlignmentPipeline.get_infer_dataset
        dataset = get_infer_dataset(params.alignment_input, params)

        dataset = torch.utils.data.DataLoader(dataset, batch_size=None)
        iterator = iter(dataset)
        counter = 0

        # Buffers for synchronization
        results = [0., 0.]

        print(f"src_file: {os.path.abspath(params.alignment_input[0])}\n"
              f"tgt_file: {os.path.abspath(params.alignment_input[1])}\n"
              f"src_ans_file: {os.path.abspath(params.test_answers[0])}\n"
              f"tgt_ans_file: {os.path.abspath(params.test_answers[1])}\n"
              f"alignment_output: {os.path.abspath(params.alignment_output)}")

        src_file = open(params.alignment_input[0], encoding="utf-8")
        tgt_file = open(params.alignment_input[1], encoding="utf-8")

        src_ans_file = None
        if os.path.exists(params.test_answers[0]):
            src_ans_file = open(params.test_answers[0], encoding="utf-8")
        
        tgt_ans_file = open(params.test_answers[1], encoding="utf-8")

        output_sentences = open(params.alignment_output + ".txt", 'w', encoding="utf-8")
        output_answers = open(params.alignment_output + "2.txt", 'w', encoding="utf-8")
        if src_ans_file:
            output_tokens = open(params.alignment_output + "3.txt", 'w', encoding="utf-8")

        while True:
            try:
                # get one batch of data
                features = next(iterator)
                features = to_cuda(features)
            except:
                break

            t = time.time()
            counter += 1

            # run mask-predict
            acc_cnt, all_cnt, state = model.cal_alignment(features)
            score = 0.0 if all_cnt == 0 else acc_cnt / all_cnt

            results[0] += acc_cnt
            results[1] += all_cnt

            source_lengths, target_lengths = features["source_mask"].sum(-1).long().tolist(), features[
                "target_mask"].sum(-1).long().tolist()

            for weight_f, weight_b, src_len, tgt_len in zip(state['f_cross_attn'], state['b_cross_attn'],
                                                            source_lengths, target_lengths):
                src = src_file.readline().strip().split()
                tgt = tgt_file.readline().strip().split()
                tgt_ans = tgt_ans_file.readline().strip().split()
                if src_ans_file:
                    src_ans = src_ans_file.readline().strip().split()

                # The "ans" file contains the position of the answer in the format idx1:idx2
                tgt_answer_position = get_answer_token_indexes(tgt_ans, tgt)
                if src_ans_file:
                    src_answer_position = get_answer_token_indexes(src_ans, src)

                # calculate alignment scores (weight_final) for each sentence pair
                weight_f, weight_b = weight_f.detach(), weight_b.detach()
                weight_f, weight_b = weight_f[-1].mean(dim=0)[:tgt_len, :src_len], weight_b[-1].mean(dim=0)[:tgt_len,
                                                                                   :src_len]
                weight_final = 2 * (weight_f * weight_b) / (weight_f + weight_b)

                # keep only relevant rows (the ones corresponding to the answer) and normalize
                weight_added_per_word = weight_final[tgt_answer_position[0]:tgt_answer_position[1]].sum(
                    dim=0) / weight_final.sum(dim=0)

                threshold = 0.3932

                first_word_in_answer = get_first_greater_than(weight_added_per_word, threshold)
                last_word_in_answer = get_last_greater_than(weight_added_per_word, threshold)

                if src_ans_file:
                    # Generate output with the tokens of the sentence and their probabilities
                    for i in range(len(src)):
                        if i < len(weight_added_per_word):
                            token = src[i]
                            value = float(weight_added_per_word[i])
                            is_ans = src_answer_position[0] <= i < src_answer_position[1]
                            output_tokens.write(f"{token} {value} {is_ans}\n")

                # Extract the answer in spanish and insert brackets into the sentence to show its position
                ans_es = ""
                sentence_with_brackets = ""
                if first_word_in_answer != -1 and last_word_in_answer != -1:
                    min_idx = max(0, first_word_in_answer)
                    max_idx = min(len(src), last_word_in_answer + 1)
                    
                    # Get answer string
                    ans_es = " ".join(src[min_idx:max_idx])

                    # Insert brackets in sentence to show answer
                    src.insert(max_idx, "}}")
                    src.insert(min_idx, "{{")
                    sentence_with_brackets = " ".join(src)

                output_sentences.write(sentence_with_brackets + '\n')
                output_answers.write(ans_es + '\n')

            t = time.time() - t
            print(f"Finished batch {counter}: {score:.3f} ({t:.3f} sec)")

        print(f"acc_rate: {0.0 if results[1] == 0 else results[0] / results[1]}")


def main() -> None:
    args = parse_args()
    params = utils.Config.read(args.config, base=args.base_config, data=args.data_config, model=args.model_config,
                               exp=args.exp)
    params.alignment_output = args.alignment_output
    gen_align(params)


if __name__ == "__main__":
    main()
