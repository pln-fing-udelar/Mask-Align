import os
import re
import random

def main() -> None:
    file1 = open("./output-indexes.txt", "r", encoding="utf-8")
    file2 = open("./answers_indexes.es", "r", encoding="utf-8")
    output_file = open("./exact-match.txt", "w", encoding="utf-8")

    lines1 = file1.readlines()
    lines2 = file2.readlines()

    right = 0
    wrong = 0

    for idx, line in enumerate(lines1):
        line1 = re.sub(r"\n", '', lines1[idx])
        line2 = re.sub(r"\n", '', lines2[idx])
        
        if not line1:
            wrong += 1
            continue

        start1 = int(line1.split(':')[0])
        end1 = int(line1.split(':')[1]) + 1
        start2 = int(line2.split(':')[0])
        end2 = int(line2.split(':')[1])

        if start1 == start2 and end1 == end2:
            right += 1
        else:
            wrong += 1

    output_file.write("The exact match measure is: " + str(right / (right + wrong)))

    file1.close()
    file2.close()
    output_file.close()

if __name__ == "__main__":
    main()
