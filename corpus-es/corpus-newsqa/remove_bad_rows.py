import os
import random
import re
import csv

### This script is used to filter the rows with bad data in newsqa.csv, creating the newsqa_filtered.csv file

csv_input = open("newsqa.csv", "r", encoding="utf8")
csv_input2 = open("newsqa.csv", "r", encoding="utf8")
csv_data = list(csv.reader(csv_input, delimiter=','))[1:]
csv_lines = csv_input2.readlines()

csv_output = open("newsqa_filtered.csv", "w", encoding="utf8")
csv_output2 = open("newsqa_bad_rows.csv", "w", encoding="utf8")

for idx, entry in enumerate(csv_data):
    if re.match(r"^(\s|\t|\n|\r)*$", str(entry[0])) == None and re.match(r"^(\s|\t|\n|\r)*$", str(entry[1])) == None and re.match(r"^(\s|\t|\n|\r)*$", str(entry[2])) == None and re.match(r"^(\s|\t|\n|\r)*$", str(entry[3])) == None and re.match(r"^(\s|\t|\n|\r)*$", str(entry[4])) == None and re.match(r"^(\s|\t|\n|\r)*$", str(entry[5])) == None:
        csv_output.write(csv_lines[idx + 1])
    else:
        csv_output2.write(csv_lines[idx + 1])

csv_input.close()
csv_input2.close()
csv_output.close()
csv_output2.close()
