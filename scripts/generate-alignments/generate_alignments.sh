#!/usr/bin/env bash

set -ex

cd corpus-es/

../scripts/generate-alignments/remove_bad_rows.py
../scripts/generate-alignments/generate_files.py

spm_encode --model=en.model --output_format=piece < sentences.en > sentences.32k.en
spm_encode --model=es.model --output_format=piece < sentences.es > sentences.32k.es

../scripts/generate-alignments/process_answer_indexes.py

../thualign/bin/generate.sh -s spanish -o output

spm_decode --model=es.model --input_format=piece < output.txt > output-plain.txt

../scripts/generate-alignments/output_brackets_to_indexes.py

sed -i '1ianswer_index_esp' output-indexes.txt

csvjoin -y 0 newsqa_filtered.csv output-indexes.txt > newsqa-es.csv
