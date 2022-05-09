#!/usr/bin/env python
import csv
import re
import sys


def main() -> None:
    with open(sys.argv[1], encoding="utf-8") as input_file, \
            open("sentences.en", "w", encoding="utf-8") as output_src_file, \
            open("sentences.es", "w", encoding="utf-8") as output_tgt_file, \
            open("answers_indexes.en", "w", encoding="utf-8") as output_ans_idx_en_file, \
            open("answers_indexes.es", "w", encoding="utf-8") as output_ans_idx_es_file:
        csv_reader_iterator = iter(csv.reader(input_file))

        next(csv_reader_iterator)  # Skip the header.

        for row in csv_reader_iterator:
            story_en = row[1]
            story_es = row[4]

            ans_en_start = story_en.find("{")
            ans_en_end = story_en.find("}")
            if ans_en_start != -1 and ans_en_end != -1:
                output_src_file.write(re.sub(r"[{}]", "", story_en) + "\n")
                output_tgt_file.write(re.sub(r"[{}]", "", story_es) + "\n")
                output_ans_idx_en_file.write(f"{ans_en_start}:{ans_en_end}\n")

            ans_es_start = story_es.find("{")
            ans_es_end = story_es.find("}")
            if ans_es_start != -1 and ans_es_end != -1:
                output_ans_idx_es_file.write(f"{ans_es_start}:{ans_es_end}\n")


if __name__ == "__main__":
    main()
