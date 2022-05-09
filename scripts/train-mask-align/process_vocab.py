#!/usr/bin/env python
import re


# For the corpus https://opus.nlpl.eu/download.php?f=WikiMatrix/v1/tmx/en-es.tmx.gz

def process_vocab(input_path: str, output_path: str) -> None:
    with open(input_path, encoding="utf-8") as input_file, open(output_path, "w", encoding="utf-8") as output_file:
        for line in input_file:
            if token := re.search(r"(.*?)\t", line).group(1):
                output_file.write(token + "\n")


def main() -> None:
    process_vocab("es.vocab", "vocab.32k.es.txt")
    process_vocab("en.vocab", "vocab.32k.en.txt")


if __name__ == "__main__":
    main()
