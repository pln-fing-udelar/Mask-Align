import os
import random
import re
import csv

answer_indexes_file = open("output.txt", "r", encoding="utf8")
test_tok_file = open("test.32k.es", "r", encoding="utf8")
test_file = open("test.es", "r", encoding="utf8")

output_src = open("output2.txt", "w", encoding="utf8")


answer_indexes = answer_indexes_file.readlies()
test_tok = test_tok_file.readlies()
test = test_file.readlies()


for idx, answer in enumerate(answer_indexes):
    ansidx1, ansidx2 = answer.split(":")[0], answer.split(":")[1]
    ans_tok = test_tok[idx][ansidx1:ansidx2]
    text_before_ans = test_tok[idx][:ansidx1]
    text_after_ans = test_tok[idx][ansidx2:]
    text = test[idx]
    
    text_before_ans = re.sub(r"▁|\s", "", text_before_ans)
    pattern1 = r'{}'.format("\s*".join(list(text_before_ans)))
    pattern2 = r'{}'.format("\s*".join(list(text_after_ans)))
    
    match1 = re.finditer(pattern1, text)
    match1 = re.finditer(pattern2, text)

    idx_start = -1
    idx_end = -1
    if match1:
        idx_start = match1.span()[1]
    else:
        print("ERRORRR")
        
    if match2:
        idx_end = match2.span()[0]
    else:
        print("ERRORRR2222")

answer_indexes_file.close()
test_tok_file.close()
test_file.close()
