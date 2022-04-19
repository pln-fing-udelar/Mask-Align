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

for i in range(0, num_sentences):
    num_words1 = len(data1[i].split(' '))
    num_words2 = len(data2[i].split(' '))
    if re.search(r'\w+', data1[i]) and re.search(r'\w+', data2[i]) and "<" not in data1[i] and "<" not in data2[i] and num_words1 > 1 and num_words1 < 120 and num_words2 > 1 and num_words2 < 120:
        random_number = random.uniform(0, 1)
        if random_number < 0.9989:
            corpus_es.write(data1[i].lower())
            corpus_en.write(data2[i].lower())
        elif random_number < 0.9978:
            validation_es.write(data1[i].lower())
            validation_en.write(data2[i].lower())        
        else:
            test_es.write(data1[i].lower())
            test_en.write(data2[i].lower())

file1.close()
file2.close()
corpus_es.close()
corpus_en.close()
validation_es.close()
validation_en.close()
test_es.close()
test_en.close()