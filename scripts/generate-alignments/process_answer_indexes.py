#!/usr/bin/env python
# This script is used to generate the following files (using the files created by the preprocess_annotated.py script):
#    - answers.en:   contains the index of the answer for each sentence, after tokenizing with sentencepiece
#    - answers.32k.en.txt:   contains the answer for each sentence in plain text, after tokenizing with sentencepiece
#    - answers.en.txt:   contains the answer for each sentence in plain text, untokenized
import re


def main(sent_untok_filename: str, sent_tok_filename: str, ans_idx_untok_filename: str,
         ans_idx_tok_filename: str, ans_tok_filename: str, ans_untok_filename: str) -> None:
    with open(sent_untok_filename, encoding="utf-8") as sentences_untokenized:
        data1 = sentences_untokenized.readlines()

    with open(sent_tok_filename, encoding="utf-8") as sentences_tokenized:
        data2 = sentences_tokenized.readlines()

    with open(ans_idx_untok_filename, encoding="utf-8") as answer_indexes_untokenized:
        data3 = answer_indexes_untokenized.readlines()

    with open(ans_idx_tok_filename, "w", encoding="utf-8") as answer_indexes_tokenized, \
            open(ans_tok_filename, "w", encoding="utf-8") as answer_tokenized, \
            open(ans_untok_filename, "w", encoding="utf-8") as answer_untokenized:
        num_sentences = min(min(len(data1), len(data2)), len(data3))
        for i in range(num_sentences):
            sentence_untok = data1[i]
            sentence_tok = data2[i]

            sentence_untok = sentence_untok.replace(r"$", "Ç")
            sentence_tok = sentence_tok.replace(r"$", "Ç")

            idx1 = int(data3[i].split(':')[0])
            idx2 = int(data3[i].split(':')[1])

            ans = sentence_untok[idx1:idx2]
            ans_fixed = re.sub(r"\?", r"\?", ans)
            ans_fixed = re.sub(r"\.", r"\.", ans_fixed)
            ans_fixed = re.sub(r"\*", r"\*", ans_fixed)
            ans_fixed = re.sub(r"\+", r"\+", ans_fixed)

            occurrences_before = re.findall(ans_fixed, sentence_untok[:idx1])
            num_before = len(occurrences_before)

            pattern1 = r"[\s▁]*".join(list(ans))
            pattern2 = r"[\s▁]*".join(list(re.sub(r"r[^\w\s]", "", ans)))

            pattern1 = re.sub(r"\?", r"\?", pattern1)
            pattern1 = re.sub(r"\.", r"\.", pattern1)
            pattern1 = re.sub(r"\+", r"\+", pattern1)
            pattern2 = re.sub(r"\?", r"\?", pattern2)
            pattern2 = re.sub(r"\.", r"\.", pattern2)
            pattern2 = re.sub(r"\+", r"\+", pattern2)

            occurrences_tokenized = list(re.finditer(pattern1, sentence_tok))

            if not occurrences_tokenized:
                occurrences_tokenized = list(re.finditer(pattern2, sentence_tok))

            match = occurrences_tokenized[num_before]

            new_idx1 = match.span()[0]
            new_idx2 = match.span()[1]

            sentence_untok = sentence_untok.replace("Ç", "$")
            sentence_tok = sentence_tok.replace("Ç", "$")

            answer_indexes_tokenized.write(str(new_idx1) + ":" + str(new_idx2) + "\n")
            answer_tokenized.write(sentence_tok[new_idx1:new_idx2] + "\n")
            answer_untokenized.write(sentence_untok[idx1:idx2] + "\n")


if __name__ == "__main__":
    main("test.en", "test.32k.en", "answers-indexes.en.txt", "answers.en", "answers.32k.en.txt", "answers.en.txt")
