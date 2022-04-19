#!/usr/bin/env bash
set -ex
python ./scripts/generate-alignments/remove_bad_rows.py
python ./scripts/generate-alignments/generate_files.py
spm_encode --model=en.model --output_format=piece < test.en > test.32k.en  
spm_encode --model=es.model --output_format=piece < test.es > test.32k.es
python ./scripts/generate-alignments/process_answer_indexes.py
mkdir -p corpus-es
mv test.32k.en test.32k.es answers.en vocab.32k.es.txt vocab.32k.en.txt corpus-es/
./thualign/bin/generate.sh -s spanish -o output.txt
spm_decode --model=es.model --input_format=piece < output.txt > output-plain.txt
python ./scripts/generate-alignments/output_brackets_to_indexes.py