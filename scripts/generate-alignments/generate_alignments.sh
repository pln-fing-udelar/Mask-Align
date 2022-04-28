#!/usr/bin/env bash
set -ex
python ./scripts/generate-alignments/remove_bad_rows.py
python ./scripts/generate-alignments/generate_files.py
spm_encode --model=en.model --output_format=piece < sentences.en > sentences.32k.en  
spm_encode --model=es.model --output_format=piece < sentences.es > sentences.32k.es
python ./scripts/generate-alignments/process_answer_indexes.py
mkdir -p corpus-es
mv sentences.32k.en sentences.32k.es answers.en vocab.32k.es.txt vocab.32k.en.txt corpus-es/
./thualign/bin/generate.sh -s spanish -o output.txt
spm_decode --model=es.model --input_format=piece < output.txt > output-plain.txt
python ./scripts/generate-alignments/output_brackets_to_indexes.py
sed -i '1ianswer_index_esp' output-indexes.txt
csvjoin -y 0 newsqa_filtered.csv output-indexes.txt  > newsqa-es.csv