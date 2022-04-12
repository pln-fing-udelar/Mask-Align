#!/usr/bin/env python
import re


def main() -> None:
    with open("output-plain.txt", encoding="utf-8") as input_file, \
            open("output-indexes.txt", "w", encoding="utf-8") as output_file, \
            open("output-answers.txt", "w", encoding="utf-8") as answer_file, \
            open("output-sentences.txt", "w", encoding="utf-8") as sentence_file:
        for line in input_file:
            match1 = re.search("{{", line)
            match2 = re.search("}}", line)
            if match1 and match2:
                start_idx = match1.span()[0]
                end_idx = match2.span()[0] - 2
                line = re.sub(r"{{", "", line)
                line = re.sub(r"}}", "", line)

                while line[start_idx] == " ":
                    start_idx += 1

                output_file.write(str(start_idx) + ":" + str(end_idx) + "\n")
                answer_file.write(line[start_idx:end_idx] + "\n")
                sentence_file.write(line)
            else:
                output_file.write("\n")
                answer_file.write("\n")
                sentence_file.write(line)


if __name__ == "__main__":
    main()
