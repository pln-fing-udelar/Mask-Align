import os
import re
import random

file1 = open("./output-test-indexes.txt", "r", encoding="utf-8")
file2 = open("./answers-indexes.es.txt", "r", encoding="utf-8")

lines1 = file1.readlines()
lines2 = file2.readlines()

right = 0
wrong = 0

for idx, line in enumerate(lines1):
    if lines1[idx] == lines2[idx]:
        right += 1
    else:
        wrong += 1
        
        
print(right / (right + wrong))
