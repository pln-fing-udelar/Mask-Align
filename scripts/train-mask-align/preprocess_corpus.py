#!/usr/bin/env python
import random
import re


# For the corpus https://opus.nlpl.eu/download.php?f=WikiMatrix/v1/tmx/en-es.tmx.gz

def main() -> None:
    with open("corpus.es", "w", encoding="utf-8") as corpus_es, \
            open("corpus.en", "w", encoding="utf-8") as corpus_en, \
            open("validation.es", "w", encoding="utf-8") as validation_es, \
            open("validation.en", "w", encoding="utf-8") as validation_en, \
            open("test.es", "w", encoding="utf-8") as test_es, \
            open("test.en", "w", encoding="utf-8") as test_en, \
            open("europarl-v7.es-en.es", encoding="utf-8") as file1, \
            open("europarl-v7.es-en.en", encoding="utf-8") as file2:

        min_word = 999999
        min_char = 999999
        max_word = 0
        max_char = 0

        for line1, line2 in zip(file1, file2):
            line1 = line1.lower()
            line2 = line2.lower()

            num_words = len(line1.split())

            max_word = max(num_words, max_word)
            max_char = max(len(line1), max_char)
            min_word = min(num_words, min_word)
            min_char = min(len(line1), min_char)

            if re.search(r"\w+", line1) \
                    and re.search(r"\w+", line1) \
                    and "<" not in line1 \
                    and "<" not in line2 \
                    and 1 < num_words < 120:
                random_number = random.uniform(0, 1)
                if random_number < 0.85:
                    corpus_es.write(line1)
                    corpus_en.write(line2)
                elif random_number < 0.95:
                    validation_es.write(line1)
                    validation_en.write(line2)
                else:
                    test_es.write(line1)
                    test_en.write(line2)

        print(max_char)
        print(max_word)
        print(min_char)
        print(min_word)


if __name__ == "__main__":
    main()
