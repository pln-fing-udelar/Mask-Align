import os
import random
import re
import csv

csv_input = open("mask-align-anotado.csv", "r", encoding="utf8")
output_src = open("source.txt", "w", encoding="utf8")
output_tgt = open("target.txt", "w", encoding="utf8")
output_ans_idx = open("answers-indexes.txt", "w", encoding="utf8")
output_ans = open("answers.txt", "w", encoding="utf8")

csv_data = list(csv.reader(csv_input, delimiter=','))[1:]

for entry in csv_data:
    ans_start = entry[1].find('{')
    ans_end = entry[1].find('}')
    if ans_start != -1 and ans_end != -1:
        output_src.write(re.sub(r'{|}', '', entry[1]) + "\n")
        output_tgt.write(re.sub(r'{|}', '', entry[4]) + "\n")
        output_ans.write(re.sub(r'{|}', '', entry[1][ans_start:ans_end]) + "\n")
        output_ans_idx.write(str(ans_start) + ":" + str(ans_end) + "\n")