import os
import re
import random

# For the corpus https://opus.nlpl.eu/download.php?f=WikiMatrix/v1/tmx/en-es.tmx.gz

sentences_untokenized = open("./test.es", "r", encoding="utf-8")
sentences_tokenized = open("./test.32k.es", "r", encoding="utf-8")
answer_indexes_untokenized = open("./answers-indexes.es.txt", "r", encoding="utf-8")
answer_indexes_tokenized = open("./answers-indexes.32k.es.txt", "w", encoding="utf-8")
answer_tokenized = open("./answers.32k.es.txt", "w", encoding="utf-8")
answer_untokenized = open("./answers.es.txt", "w", encoding="utf-8")

data1 = sentences_untokenized.readlines()
data2 = sentences_tokenized.readlines()
data3 = answer_indexes_untokenized.readlines()
num_sentences = min(min(len(data1), len(data2)), len(data3))

for i in range(0, num_sentences):
    sentence_untok = data1[i]
    sentence_tok = data2[i]
    
    sentence_untok = sentence_untok.replace("$", r"Ç")
    sentence_tok = sentence_tok.replace("$", r"Ç")
    
    idx1 = int(data3[i].split(':')[0])
    idx2 = int(data3[i].split(':')[1]) - 1
    
    ans = r'{}'.format(sentence_untok[idx1:idx2])
    #ans = re.sub(r"\(", r"\\(", ans)
    #ans = re.sub(r"\)", r"\\)", ans)
    
    
    occurences_before = re.findall(ans, sentence_untok[:idx1])
    num_before = len(occurences_before)
        
    pattern1 = r'{}'.format("[\s▁]*".join(list(ans)))
    pattern2 = r'{}'.format("[\s▁]*".join(list(re.sub("[^\w\s]", "", ans))))

    ocurrences_tokenized = list(re.finditer(pattern1, sentence_tok))
    
    if len(ocurrences_tokenized) == 0:
        ocurrences_tokenized = list(re.finditer(pattern2, sentence_tok))
            
    match = ocurrences_tokenized[num_before]
    
    new_idx1 = match.span()[0]
    new_idx2 = match.span()[1]

    sentence_untok = sentence_untok.replace("Ç", "$")
    sentence_tok = sentence_tok.replace("Ç", "$")

    answer_indexes_tokenized.write(str(new_idx1) + ":" + str(new_idx2) + "\n")
    answer_tokenized.write(sentence_tok[new_idx1:new_idx2] + "\n")
    answer_untokenized.write(sentence_untok[idx1:idx2] + "\n")


sentences_untokenized.close()
sentences_tokenized.close()
answer_indexes_untokenized.close()
answer_indexes_tokenized.close()