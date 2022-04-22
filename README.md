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

We need a trained Mask-Align model to align translations between English and Spanish. To download the pretrained model, run the following commands:

```bash
mkdir -p spanish-output/output
curl -o spanish-output/output/model-1.pt https://www.fing.edu.uy/owncloud/index.php/s/siRkUqxnwmdtfaJ/download
```

Alternatively, follow these steps to train it yourself.

### Prepare the Corpus

1. Download the [Europarl Spanish-English parallel corpus](https://www.statmt.org/europarl/v7/es-en.tgz).
2. Run the following script to do some preprocessing, learn the vocabulary, tokenize the sentences, and split the corpus:

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

6. The model is saved in a folder created in the root directory of the repository.

### Test the alignments

1. Run:

   ```bash
   ./thualign/bin/test.sh -s spanish -gvt
   ``` 

2. The alignments are generated in `test/alignments.txt`, where the model was saved.
3. To see the alignments in an interactive way, run:

   ```bash
   ./thualign/scripts/visualize.py spanish/output/test/alignment_vizdata.pt
   ```

## Generating the Answer Alignments for NewsQA-es

Run the following script to generate the answer alignments for the NewsQA-es dataset. You should have a trained Mask-Align 
model and have the `newsqa.csv` file.

```bash
./scripts/generate-alignments/generate_alignments.sh
```

The following three files are generated:  

* `output-indexes.txt`: the indexes of the answers in Spanish.  
* `output-answers.txt`: the answers in Spanish (in plain text).  
* `output-sentences.txt`: the sentences in Spanish (not tokenized).

### Generate the final merged CSV file

Finally, run these commands to generate the `newsqa-es.csv` file, a new version of `newsqa_filtered.csv` which has the columns with the answers in Spanish.

```bash
sed -i '1ianswer_index_esp' output-indexes.txt
csvjoin -y 0 newsqa_filtered.csv output-indexes.txt  > newsqa-es.csv
```