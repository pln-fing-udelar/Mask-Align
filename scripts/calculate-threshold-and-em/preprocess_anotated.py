#!/usr/bin/env python
import os
import random
import re
import csv
import sys

def main(input_file) -> None:
    csv_input = open(input_file, "r", encoding="utf8")
    output_src = open("sentences.en", "w", encoding="utf8")
    output_tgt = open("sentences.es", "w", encoding="utf8")
    output_ans_idx_en = open("answers_indexes.en", "w", encoding="utf8")
    output_ans_idx_es = open("answers_indexes.es", "w", encoding="utf8")

    csv_data = list(csv.reader(csv_input, delimiter=','))[1:]

    for entry in csv_data:
        ans_start = entry[1].find('{')
        ans_end = entry[1].find('}')
        if ans_start != -1 and ans_end != -1:
            output_src.write(re.sub(r'{|}', '', entry[1]) + "\n")
            output_tgt.write(re.sub(r'{|}', '', entry[4]) + "\n")
            output_ans_idx_en.write(str(ans_start) + ":" + str(ans_end) + "\n")

    for entry in csv_data:
        ans_start = entry[4].find('{')
        ans_end = entry[4].find('}')
        if ans_start != -1 and ans_end != -1:
            output_ans_idx_es.write(str(ans_start) + ":" + str(ans_end) + "\n")
            
    csv_input.close()
    output_src.close()
    output_tgt.close()
    output_ans_idx_en.close()
    output_ans_idx_es.close()

if __name__ == "__main__":
    main(sys.argv[1])
