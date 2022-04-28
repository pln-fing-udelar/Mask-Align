#!/usr/bin/env bash

set -ex

mkdir -p corpus-es
cd corpus-es/

wget -qO- https://www.statmt.org/europarl/v7/es-en.tgz | tar -xz

../scripts/train-mask-align/split_corpus.py

spm_train --input=corpus.en --model_prefix=en --vocab_size=32000 --character_coverage=1.0 --model_type=unigram
spm_train --input=corpus.es --model_prefix=es --vocab_size=32000 --character_coverage=1.0 --model_type=unigram

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
