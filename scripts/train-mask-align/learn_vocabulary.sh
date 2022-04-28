#!/usr/bin/env bash

set -ex

mkdir -p corpus-es
cd corpus-es/

wget -qO- https://www.statmt.org/europarl/v7/es-en.tgz | tar -xz

../scripts/train-mask-align/split_corpus.py

spm_train --input=corpus.en --model_prefix=en --vocab_size=32000 --character_coverage=1.0 --model_type=unigram
spm_train --input=corpus.es --model_prefix=es --vocab_size=32000 --character_coverage=1.0 --model_type=unigram
