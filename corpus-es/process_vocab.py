import os
import re
import random

# For the corpus https://opus.nlpl.eu/download.php?f=WikiMatrix/v1/tmx/en-es.tmx.gz

vocab_es = open("./es.vocab", "r", encoding="utf-8")
vocab_en = open("./en.vocab", "r", encoding="utf-8")


vocab_es_final = open("./vocab.32k.es.txt", "w", encoding="utf-8")
vocab_en_final = open("./vocab.32k.en.txt", "w", encoding="utf-8")

data_es = vocab_es.readlines()
data_en = vocab_en.readlines()

for i in range(0, len(data_es)):
    token = re.search(r'(.*?)\t.*', data_es[i]).group(1)
    if token:
        vocab_es_final.write(token + '\n')

for i in range(0, len(data_en)):
    token = re.search(r'(.*?)\t.*', data_en[i]).group(1)
    if token:
        vocab_en_final.write(token + '\n')

vocab_es.close()
vocab_en.close()
vocab_es_final.close()
vocab_en_final.close()
