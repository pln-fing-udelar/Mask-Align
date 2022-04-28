# Mask-Align for NewsQA-es

This repo forks [THUNLP-MT/Mask-Align](https://github.com/THUNLP-MT/Mask-Align) to adapt it to translate
the [NewsQA](https://www.microsoft.com/en-us/research/project/newsqa-dataset/) reading comprehension dataset to Spanish
(see [the NewsQA-es repo](https://github.com/pln-fing-udelar/newsqa-es) for more info). Mask-Align is an algorithm 
that aligns translations to a token level, which allows us to find the English answer span
inside the translated Spanish text.

## Setup

First, clone this repo:

```bash
git clone https://github.com/pln-fing-udelar/Mask-Align
cd Mask-Align/
```

Then, using [Conda](https://docs.conda.io/en/latest/index.html), run:

```bash
conda env create
conda activate mask-align
```

## Training Mask-Align in English-Spanish

We need a trained Mask-Align model to align translations between English and Spanish. To download the pretrained model, run the following commands:

```bash
mkdir -p spanish-output/output
curl -o spanish-output/output/model-1.pt https://www.fing.edu.uy/owncloud/index.php/s/siRkUqxnwmdtfaJ/download
```

Alternatively, follow these steps to train it yourself.

### Prepare the Corpus

Run the following script to download the [Europarl Spanish-English parallel corpus](https://www.statmt.org/europarl/v7/es-en.tgz), do some preprocessing, learn the vocabulary, tokenize the sentences, and split the corpus:

```bash
./scripts/train-mask-align/preprocess_europarl.sh
```

### Train the Model

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

6. The model checkpoints are saved under `spanish-output/output/`. The latest one has the highest number in the 
   filename. When testing or generating, the codebase selects the best or the latest model automatically.

### Test the alignments

1. Run:

   ```bash
   ./thualign/bin/test.sh -s spanish -gvt
   ``` 

2. The alignments are generated in `spanish-output/output/test/alignments.txt`.
3. To see the alignments in an interactive way, run:

   ```bash
   ./thualign/scripts/visualize.py spanish-output/output/test/alignment_vizdata.pt
   ```

## Generating the Answer Alignments for NewsQA-es

Run the following script to generate the answer alignments for the NewsQA-es dataset. You should have a trained
Mask-Align model and have the `newsqa.csv` file.

```bash
./scripts/generate-alignments/generate_alignments.sh
```

The following 4 files are going to be generated:  

* `output-indexes.txt`: the indexes of the answers in Spanish.  
* `output-answers.txt`: the answers in Spanish (in plain text).  
* `output-sentences.txt`: the sentences in Spanish (not tokenized).
* `newsqa-es.csv`: a new version of `newsqa_filtered.csv` which has the columns with the answers in Spanish.
