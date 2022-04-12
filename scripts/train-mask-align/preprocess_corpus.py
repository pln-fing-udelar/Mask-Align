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
            open("test.en", "w", encoding="utf-8") as test_en:
        with open("europarl-v7.es-en.es", encoding="utf-8") as file:
            data1 = file.readlines()
        with open("europarl-v7.es-en.en", encoding="utf-8") as file:
            data2 = file.readlines()

        min_word = 999999
        min_char = 999999
        max_word = 0
        max_char = 0

        for i in range(min(len(data1), len(data2))):
            num_words = len(data1[i].split())
            if num_words > max_word:
                max_word = num_words
            if len(data1[i]) > max_char:
                max_char = len(data1[i])
            if num_words < min_word:
                min_word = num_words
            if len(data1[i]) < min_char:
                min_char = len(data1[i])
            if re.search(r"\w+", data1[i]) \
                    and re.search(r"\w+", data1[i]) \
                    and "<" not in data1[i] \
                    and "<" not in data2[i] \
                    and 1 < num_words < 120:
                random_number = random.uniform(0, 1)
                if random_number < 0.85:
                    corpus_es.write(data1[i].lower())
                    corpus_en.write(data2[i].lower())
                elif random_number < 0.95:
                    validation_es.write(data1[i].lower())
                    validation_en.write(data2[i].lower())
                else:
                    test_es.write(data1[i].lower())
                    test_en.write(data2[i].lower())

        print(max_char)
        print(max_word)
        print(min_char)
        print(min_word)


if __name__ == "__main__":
    main()
