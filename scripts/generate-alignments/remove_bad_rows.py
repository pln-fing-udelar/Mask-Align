#!/usr/bin/env python
# This script is used to filter the rows with bad data in newsqa.csv, creating the newsqa_filtered.csv file
import csv
import re


def main() -> None:
    with open("newsqa.csv", encoding="utf8") as csv_input, \
            open("newsqa.csv", encoding="utf8") as csv_input2, \
            open("newsqa_filtered.csv", "w", encoding="utf8") as csv_output, \
            open("newsqa_bad_rows.csv", "w", encoding="utf8") as csv_output2:
        for i, (row, csv_line) in enumerate(zip(csv.reader(csv_input), csv_input2)):
            if i == 0:
                csv_output.write(csv_line)
                csv_output2.write(csv_line)
            else:
                ans_start = -1
                ans_end = -1
                if indexes := re.search(r"\d+:\d+", row[5]):
                    start_end_str = indexes.group(0).split(":")
                    ans_start = int(start_end_str[0])
                    ans_end = int(start_end_str[1])

                if any(re.match(r"^(\s|\t|\n|\r)*$", str(row[j])) for j in range(6)) is None \
                        and "*" not in str(row[2]) \
                        and "Ã" not in str(row[3]) \
                        and i not in {33677, 33676, 116925, 116926} \
                        and ans_start > -1 \
                        and ans_end > -1:
                    output_file = csv_output
                else:
                    output_file = csv_output2
                output_file.write(csv_line)


if __name__ == "__main__":
    main()
