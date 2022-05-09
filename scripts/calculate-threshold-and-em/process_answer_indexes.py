#!/usr/bin/env python
import re


def process_answer_indexes(sentences, sentences_tok, answer_indexes, answer_indexes_tok):
    with open(sentences, encoding="utf-8") as sentences_file, \
            open(sentences_tok, encoding="utf-8") as sentences_tokenized_file, \
            open(answer_indexes, encoding="utf-8") as answer_indexes_file, \
            open(answer_indexes_tok, "w", encoding="utf-8") as answer_indexes_tokenized_file:
        for sentence, tokenizer_sentence, indices_str in zip(sentences_file, sentences_tokenized_file,
                                                             answer_indexes_file):
            sentence = sentence.replace("$", "Ç")
            tokenizer_sentence = tokenizer_sentence.replace("$", "Ç")

            indices_pair_str = indices_str.split(":", maxsplit=1)
            start_index, end_index = int(indices_pair_str[0]), int(indices_pair_str[1]) - 1
            ans = sentence[start_index:end_index]

            occurrences_before = re.findall(ans, sentence[:start_index])
            num_before = len(occurrences_before)

            occurrences_tokenized = list(re.finditer(r"[\s▁]*".join(ans), tokenizer_sentence)) or list(
                re.finditer(r"[\s▁]*".join(iter(re.sub(r"[^\w\s]", "", ans))), tokenizer_sentence))

            start_token_idx, end_token_idx = occurrences_tokenized[num_before].span()[:2]

            answer_indexes_tokenized_file.write(f"{start_token_idx}:{end_token_idx}\n")


def main() -> None:
    process_answer_indexes("sentences.es", "sentences.32k.es", "answers_indexes.es", "answers.es")
    process_answer_indexes("sentences.en", "sentences.32k.en", "answers_indexes.en", "answers.en")


if __name__ == "__main__":
    main()
