import random

test_es = open("./test.32k.es", "r", encoding="utf-8")
test_en = open("./test.32k.en", "r", encoding="utf-8")

test_es2 = open("./test-short.32k.es", "w", encoding="utf-8")
test_en2 = open("./test-short.32k.en", "w", encoding="utf-8")

data_es = test_es.readlines()
data_en = test_en.readlines()

num_sentences = min(len(data_es), len(data_en))

print(num_sentences)

for i in range(0, num_sentences):
    num_words = len(data_es[i].split(' '))
    if num_words < 120 and random.uniform(0, 1) < 0.006:
        test_es2.write(data_es[i].lower())
        test_en2.write(data_en[i].lower())

test_es.close()
test_en.close()
test_es2.close()
test_en2.close()
