#!/usr/bin/env python
import os
import re
import random

# For the corpus https://opus.nlpl.eu/download.php?f=WikiMatrix/v1/tmx/en-es.tmx.gz

def process_answer_indexes(sentences, sentences_tok, answer_indexes, answer_indexes_tok):
    sentences_untokenized = open(sentences, "r", encoding="utf-8")
    sentences_tokenized = open(sentences_tok, "r", encoding="utf-8")
    answer_indexes_untokenized = open(answer_indexes, "r", encoding="utf-8")
    answer_indexes_tokenized = open(answer_indexes_tok, "w", encoding="utf-8")

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

    sentences_untokenized.close()
    sentences_tokenized.close()
    answer_indexes_untokenized.close()
    answer_indexes_tokenized.close()


def main() -> None:
    process_answer_indexes("sentences.es", "sentences.32k.es", "answers_indexes.es", "answers.es")
    process_answer_indexes("sentences.en", "sentences.32k.en", "answers_indexes.en", "answers.en")


if __name__ == "__main__":
    main()
