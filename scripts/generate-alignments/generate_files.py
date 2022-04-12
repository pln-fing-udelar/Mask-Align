#!/usr/bin/env python
### This script is used to generate the following files (using the csv file newsqa_filtered.csv):
###   - test.en, test.es:   they contain the sentences of the corpus
###   - answers.en.txt:   it contains the answer in plain text for each of the sentences
###   - answers-indexes.en.txt:   it contains the index of the answer for each of the sentences
import csv
import re


def extract_first_answer(text: str) -> str:
    first_answer = re.search(r"(.*?)##", text)
    return first_answer.group(1) if first_answer else return text

def main() -> None:
    with open("newsqa_filtered.csv", encoding="utf8") as csv_input:
        csv_data = list(csv.reader(csv_input, delimiter=','))[1:]

    with open("test.en", "w", encoding="utf8") as output_src,
            open("test.es", "w", encoding="utf8") as output_tgt,
            open("answers-indexes.en.txt", "w", encoding="utf8") as output_ans_idx_en,
            open("answers.en.txt", "w", encoding="utf8") as output_ans_en:
    for entry in csv_data:
        indexes = re.search(r"\d+:\d+", entry[5])
        if indexes:
            ans_start = indexes.group(0).split(":")[0]
            ans_end = indexes.group(0).split(":")[1]
            if int(ans_start) > -1 and int(ans_end) > -1:
                output_ans_en.write(extract_first_answer(entry[2]) + "\n")
                output_ans_idx_en.write(str(ans_start) + ":" + str(ans_end) + "\n")
                output_src.write(extract_first_answer(entry[3]) + "\n")
                output_tgt.write(extract_first_answer(entry[4]) + "\n")


if __name__ == "__main__":
    main()
