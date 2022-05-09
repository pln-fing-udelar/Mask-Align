#!/usr/bin/env python
"""Script used to filter the rows with bad data in `newsqa.csv`, creating the `newsqa_filtered.csv` file."""
import csv
import re


def main() -> None:
    with open("newsqa.csv", encoding="utf-8") as input_file:
        rows = [[entry.strip() for entry in row] for row in csv.reader(input_file)][1:]
    with open("newsqa.csv", encoding="utf-8") as input_file:
        lines = input_file.readlines()

    with open("newsqa_filtered.csv", "w", encoding="utf-8") as filtered_output_file, \
            open("newsqa_bad_rows.csv", "w", encoding="utf-8") as bad_rows_output_file:
        filtered_output_file.write(lines[0])
        bad_rows_output_file.write(lines[0])

        lines = lines[1:]

        for i, (line, row) in enumerate(zip(lines, rows)):
            question_id, question, answer, sentences, sentence_es, answer_offsets_sentence = row[:6]
            if question_id and question and answer and sentences and sentence_es and answer_offsets_sentence \
                    and "*" not in answer and "Ã" not in sentences and i not in {33676, 33677, 116925, 116926} \
                    and re.search(r"\d+:\d+", answer_offsets_sentence):
                output_file = filtered_output_file
            else:
                output_file = bad_rows_output_file

            output_file.write(line)


if __name__ == "__main__":
    main()
