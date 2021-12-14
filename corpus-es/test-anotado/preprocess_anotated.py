import os
import random
import re
import csv

csv_input = open("mask-align-anotado.csv", "r", encoding="utf8")
output_src = open("test.en", "w", encoding="utf8")
output_tgt = open("test.es", "w", encoding="utf8")
output_ans_idx_en = open("answers-indexes.en.txt", "w", encoding="utf8")
output_ans_en = open("answers.en.txt", "w", encoding="utf8")

output_ans_idx_es = open("answers-indexes.es.txt", "w", encoding="utf8")
output_ans_es = open("answers.es.txt", "w", encoding="utf8")

csv_data = list(csv.reader(csv_input, delimiter=','))[1:]

for entry in csv_data:
    ans_start = entry[1].find('{')
    ans_end = entry[1].find('}')
    if ans_start != -1 and ans_end != -1:
        output_src.write(re.sub(r'{|}', '', entry[1]) + "\n")
        output_tgt.write(re.sub(r'{|}', '', entry[4]) + "\n")
        output_ans_en.write(re.sub(r'{|}', '', entry[1][ans_start:ans_end]) + "\n")
        output_ans_idx_en.write(str(ans_start) + ":" + str(ans_end) + "\n")

for entry in csv_data:
    ans_start = entry[4].find('{')
    ans_end = entry[4].find('}')
    if ans_start != -1 and ans_end != -1:
        output_ans_es.write(re.sub(r'{|}', '', entry[4][ans_start:ans_end]) + "\n")
        output_ans_idx_es.write(str(ans_start) + ":" + str(ans_end) + "\n")
        
csv_input.close()
output_src.close()
output_tgt.close()
output_ans_idx_en.close()
output_ans_en.close()
output_ans_idx_es.close()
output_ans_es.close()