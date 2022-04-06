import os
import re
import random

# For the corpus https://opus.nlpl.eu/download.php?f=WikiMatrix/v1/tmx/en-es.tmx.gz

corpus_es = open("./corpus.es", "w", encoding="utf-8")
corpus_en = open("./corpus.en", "w", encoding="utf-8")
validation_es = open("./validation.es", "w", encoding="utf-8")
validation_en = open("./validation.en", "w", encoding="utf-8")
test_es = open("./test.es", "w", encoding="utf-8")
test_en = open("./test.en", "w", encoding="utf-8")

file1 = open("./europarl-v7.es-en.es", "r", encoding="utf-8")
file2 = open("./europarl-v7.es-en.en", "r", encoding="utf-8")
data1 = file1.readlines()
data2 = file2.readlines()
num_sentences = min(len(data1), len(data2))


min_word = 999999
min_char = 999999
max_word = 0
max_char = 0
for i in range(0, num_sentences):
    num_words = len(data1[i].split(' '))
    if num_words > max_word:
        max_word = num_words
    if len(data1[i]) > max_char:
        max_char = len(data1[i])
    if num_words < min_word:
        min_word = num_words
    if len(data1[i]) < min_char:
        min_char = len(data1[i])
    if re.search(r'\w+', data1[i]) and re.search(r'\w+', data1[i]) and "<" not in data1[i] and "<" not in data2[i] and num_words > 1 and num_words < 120:
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

file1.close()
file2.close()
corpus_es.close()
corpus_en.close()
validation_es.close()
validation_en.close()
test_es.close()
test_en.close()
