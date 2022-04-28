#!/usr/bin/env bash

set -ex

../scripts/train-mask-align/process_vocab.py

sed -i 's/<s>/<pad>/g' vocab.32k.es.txt
sed -i 's/<\/s>/<eos>/g' vocab.32k.es.txt
sed -i 's/<s>/<pad>/g' vocab.32k.en.txt
sed -i 's/<\/s>/<eos>/g' vocab.32k.en.txt

spm_encode --model=en.model --output_format=piece < corpus.en > corpus.32k.en
spm_encode --model=en.model --output_format=piece < validation.en > validation.32k.en
spm_encode --model=en.model --output_format=piece < test.en > test.32k.en

spm_encode --model=es.model --output_format=piece < corpus.es > corpus.32k.es
spm_encode --model=es.model --output_format=piece < validation.es > validation.32k.es
spm_encode --model=es.model --output_format=piece < test.es > test.32k.es

../thualign/scripts/shuffle_corpus.py --corpus corpus.32k.es corpus.32k.en

sed -i -e 's/<s>/<eos>/' -e 's/<s\/>/<pad>/' corpus.32k.en
sed -i -e 's/<s>/<eos>/' -e 's/<s\/>/<pad>/' validation.32k.en
sed -i -e 's/<s>/<eos>/' -e 's/<s\/>/<pad>/' test.32k.en

sed -i -e 's/<s>/<eos>/' -e 's/<s\/>/<pad>/' corpus.32k.es
sed -i -e 's/<s>/<eos>/' -e 's/<s\/>/<pad>/' validation.32k.es
sed -i -e 's/<s>/<eos>/' -e 's/<s\/>/<pad>/' test.32k.es
