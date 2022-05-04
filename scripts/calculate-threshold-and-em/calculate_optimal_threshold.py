import os
import re
import random

def main() -> None:
    data = open("./output3.txt", "r", encoding="utf-8")
    output_file = open("./threshold.txt", "w", encoding="utf-8")
    lines = data.readlines()

    num_true = 0
    num_lines = 0

    lines = sorted(lines, key=lambda line: float(line.split(" ")[1]))

    for idx, line in enumerate(lines):
        num_lines += 1
        info = line.split(" ")
        if re.sub(r"[^\w]", "", info[2]) == "True":
            num_true += 1

    num_true_so_far = 0
    num_false_so_far = 0
    num_lines_so_far = 0

    max_acc = 0
    best_threshold = -1

    for idx, line in enumerate(lines):
        info = line.split(" ")
        
        num_lines_so_far += 1
        if re.sub(r"[^\w]", "", info[2]) == "True":
            num_true_so_far += 1
        else:
            num_false_so_far += 1
        
        if idx == len(lines)-1:
            continue
        
        
        threshold = (float(lines[idx+1].split(" ")[1]) + float(lines[idx].split(" ")[1])) / 2.0
        
        
        acc  = (num_false_so_far / num_lines_so_far) * num_lines_so_far / num_lines
        acc += ((num_true - num_true_so_far) / (num_lines - num_lines_so_far)) * (num_lines - num_lines_so_far) / num_lines
        
        if acc > max_acc:
            max_acc = acc
            best_threshold = threshold

    output_file.write("The best threshold is: " + str(best_threshold) + "\n")
    output_file.write("The accuracy of this threshold is: " + str(max_acc))

    data.close()
    output_file.close()

if __name__ == "__main__":
    main()
