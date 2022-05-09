#!/usr/bin/env bash

set -ex

cd corpus-es/

curl -o news-qa-questions-test.csv https://www.fing.edu.uy/owncloud/index.php/s/gxEGql3brGqX1os/download

../scripts/calculate-threshold-and-em/preprocess_annotated.py news-qa-questions-test.csv

spm_encode --model=en.model --output_format=piece < sentences.en > sentences.32k.en
spm_encode --model=es.model --output_format=piece < sentences.es > sentences.32k.es

../scripts/calculate-threshold-and-em/process_answer_indexes.py

pushd .. > /dev/null
./thualign/bin/generate.sh -s spanish -o corpus-es/output
popd > /dev/null

spm_decode --model=es.model --input_format=piece < output.txt > output-plain.txt

../scripts/generate-alignments/output_brackets_to_indexes.py

sed -i '1ianswer_index_esp' output-indexes.txt

csvjoin -y 0 newsqa_filtered.csv output-indexes.txt > newsqa-es.csv

../scripts/calculate-threshold-and-em/calculate_em.py
