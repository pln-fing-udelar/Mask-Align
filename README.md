# Mask-Align for NewsQA-es

This repo forks [THUNLP-MT/Mask-Align](https://github.com/THUNLP-MT/Mask-Align) to adapt it to translate
the [NewsQA](https://www.microsoft.com/en-us/research/project/newsqa-dataset/) reading comprehension dataset to Spanish.
Mask-Align is an algorithm that aligns translations to a token level, which allows us to find the English answer span
inside the translated Spanish text.

## Setup

First, clone this repo:

```bash
git clone https://github.com/pln-fing-udelar/Mask-Align
cd Mask-Align/
```

Then, using [Conda](https://docs.conda.io/en/latest/index.html), run:

```bash
conda env update
conda activate mask-align
```

## Training Mask-Align in English-Spanish

TODO: provide a pretrained model.

Follow these steps to train a Mask-Align model to align translations between English and Spanish.

### Prepare the corpus

1. Download the [Europarl Spanish-English parallel corpus](https://www.statmt.org/europarl/v7/es-en.tgz).
2. Remove the sentences that don't form a pair (the sentences that correspond with an empty line).
3. Remove sentences of length 1.
4. Remove sentences that contain tags (characters "<" and ">").
5. Split the corpus into test, train and val. A good size can be 2000 sentences for test and 2000 for val. Name the
   files `corpus.es`, `validacion.es`, `test.es`, `corpus.en`, `validacion.en` and `test.en`.
7. Run the following commands, to learn the vocabulary, tokenize the sentences, and shuffle the corpus:

  ```bash
  spm_train --input=corpus.en --model_prefix=en --vocab_size=32000 --character_coverage=1.0 --model_type=unigram
  spm_train --input=corpus.es --model_prefix=es --vocab_size=32000 --character_coverage=1.0 --model_type=unigram
  spm_encode --model=en.model --output_format=piece < corpus.en > corpus.32k.en
  spm_encode --model=en.model --output_format=piece < validation.en > validation.32k.en
  spm_encode --model=en.model --output_format=piece < test.en > test.32k.en
  spm_encode --model=es.model --output_format=piece < corpus.es > corpus.32k.es
  spm_encode --model=es.model --output_format=piece < validation.es > validation.32k.es
  spm_encode --model=es.model --output_format=piece < test.es > test.32k.es
  python thualign/scripts/shuffle_corpus.py --corpus corpus.32k.es corpus.32k.en
  sed -i -e 's/<s>/<eos>/' -e 's/<s\/>/<pad>/' corpus.32k.en
  sed -i -e 's/<s>/<eos>/' -e 's/<s\/>/<pad>/' validation.32k.en
  sed -i -e 's/<s>/<eos>/' -e 's/<s\/>/<pad>/' test.32k.en
  sed -i -e 's/<s>/<eos>/' -e 's/<s\/>/<pad>/' corpus.32k.es
  sed -i -e 's/<s>/<eos>/' -e 's/<s\/>/<pad>/' validation.32k.es
  sed -i -e 's/<s>/<eos>/' -e 's/<s\/>/<pad>/' test.32k.es
  ```

### Train the model

Note you need a computer with a CUDA-capable GPU to train the model.

1. In the config file [`thualign/configs/user/spanish.config`](thualign/configs/user/spanish.config), specify the
   location of the following files:

   * `corpus.32k.es.shuf`
   * `corpus.32k.en.shuf`
   * `validation.32k.es`
   * `validation.32k.en`
   * `test.32k.es`
   * `test.32k.en`
   * `es.vocab`
   * `en.vocab`

2. In `device_list` specify the number of GPUs.
3. In `batch_size` choose the highest value that doesn't make the training stop due to lack of memory (try different
   numbers).
4. The value of `update_cycle` must be 36000 / batch_size.
5. Run:

   ```bash
   ./thualign/bin/train.sh -s spanish
   ```

6. The model is saved in a folder created in the root directory of the repository.

## Generating the answer alignments

TODO
