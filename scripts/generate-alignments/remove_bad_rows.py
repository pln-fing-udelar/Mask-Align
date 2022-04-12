#!/usr/bin/env python
# This script is used to filter the rows with bad data in newsqa.csv, creating the newsqa_filtered.csv file
import csv
import re


def main() -> None:
    with open("newsqa.csv", encoding="utf8") as csv_input:
        csv_data = list(csv.reader(csv_input, delimiter=','))

    with open("newsqa.csv", encoding="utf8") as csv_input2:
        csv_lines = csv_input2.readlines()

    with open("newsqa_filtered.csv", "w", encoding="utf8") as csv_output,
            open("newsqa_bad_rows.csv", "w", encoding="utf8") as csv_output2:
        csv_output.write(csv_lines[0])
        csv_output2.write(csv_lines[0])

        for idx, entry in enumerate(csv_data[1:]):
            ans_start = -1
            ans_end = -1
            indexes = re.search(r"\d+:\d+", entry[5])
            if indexes:
                start_end_str = indexes.group(0).split(":")
                ans_start = int(start_end_str[0])
                ans_end = int(start_end_str[1])

            if re.match(r"^(\s|\t|\n|\r)*$", str(entry[0])) is None and re.match(r"^(\s|\t|\n|\r)*$", str(entry[1])) is None and re.match(r"^(\s|\t|\n|\r)*$", str(entry[2])) is None and re.match(r"^(\s|\t|\n|\r)*$", str(entry[3])) is None and re.match(r"^(\s|\t|\n|\r)*$", str(entry[4])) is None and re.match(r"^(\s|\t|\n|\r)*$", str(entry[5])) is None and "*" not in str(entry[2]) and "Ã" not in str(entry[3]) and idx != 33676 and idx != 33677 and idx != 116925 and idx != 116926 and ans_start > -1 and ans_end > -1:                
                output_file = csv_output
            else:
                output_file = csv_output2
            output_file.write(csv_lines[idx + 1])


if __name__ == "__main__":
    main()
