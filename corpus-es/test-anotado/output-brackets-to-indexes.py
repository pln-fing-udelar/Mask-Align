import os
import re
import random


input_file = open("./output-test.txt", "r", encoding="utf-8")
output_file = open("./output-test-indexes.txt", "w", encoding="utf-8")
answer_file = open("./output-test-answers.txt", "w", encoding="utf-8")
sentence_file = open("./output-test-sentences.txt", "w", encoding="utf-8")

lines = input_file.readlines()

for idx, line in enumerate(lines):
    match1 = re.search("{{", line)
    start_idx = match1.span()[0]
    line = re.sub(r"{{", "", line)
    
    if idx == 0:
        print(line)
        
    
    match2 = re.search("}}", line)
    end_idx = match2.span()[0] + 1
    line = re.sub(r"}}", "", line)

    if idx == 0:
        print(match2)
        print(start_idx)
        print(end_idx)

    while line[start_idx] == " ":
        start_idx += 1
    
    if idx == 0:
        print(start_idx)
        print(end_idx)
    
    output_file.write(str(start_idx) + ":" + str(end_idx) + "\n")
    answer_file.write(line[start_idx:end_idx] + "\n")
    sentence_file.write(line)