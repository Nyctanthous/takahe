<h1 align="center">takahe3</h1>

### Unsupervised multi-sentence compression

`takahe3` is a Python3 conversion of the [takahe](https://github.com/boudinfl/takahe) multi-sentence compression package. Given a set of redundant sentences, a word-graph is constructed by iteratively adding sentences to it. The best compression is obtained by finding the shortest path in the word graph. The original algorithm was published and described in:

* Katja Filippova, Multi-Sentence Compression: Finding Shortest Paths in Word Graphs, *Proceedings of the 23rd International Conference on Computational Linguistics (Coling 2010)*, pages 322-330, 2010.

A keyphrase-based reranking method can be applied to generate more informative compressions. The reranking method is described in:

* Florian Boudin and Emmanuel Morin, Keyphrase Extraction for N-best Reranking in Multi-Sentence Compression, *Proceedings of the 2013 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT 2013)*, 2013.


### Requirements

+ Python 3.5+

All other requirements will be automatically acquired by `pip`; see `requirements.txt` for a complete list of all requirements that will be automatically obtained.


### Installation

You can install from this github repository with

```bash
git clone https://github.com/Nyctanthous/takahe3.git
cd takahe3
pip install .
```

Additionally, be aware that this package expects Part-of-Speech (POS) tags along with every word. `nltk` is a good choice for this task.


## Example

A typical usage of this module is:

```python
from takahe3.takahe import WordGraph, KeyphraseReranker

sentences = ["The/DT wife/NN of/IN a/DT former/JJ U.S./NNP president/NN \
              Bill/NNP Clinton/NNP Hillary/NNP Clinton/NNP visited/VBD \
              China/NNP last/JJ Monday/NNP ./PUNCT", "Hillary/NNP Clinton/NNP \
              wanted/VBD to/TO visit/VB China/NNP last/JJ month/NN but/CC \
              postponed/VBD her/PRP$ plans/NNS till/IN Monday/NNP last/JJ \
              week/NN ./PUNCT", "Hillary/NNP Clinton/NNP paid/VBD a/DT \
              visit/NN to/TO the/DT People/NNP Republic/NNP of/IN China/NNP \
              on/IN Monday/NNP ./PUNCT", "Last/JJ week/NN the/DT \
              Secretary/NNP of/IN State/NNP Ms./NNP Clinton/NNP visited/VBD \
              Chinese/JJ officials/NNS ./PUNCT"]

# Create a word graph from the set of sentences with parameters :
# - minimal number of words in the compression : 6
# - language of the input sentences : en (english)
# - POS tag for punctuation marks : PUNCT
compresser = WordGraph(sentences, nb_words=6, lang='en', punct_tag="PUNCT")

# Get the 50 best paths
candidates = compresser.get_compression(50)

# 1. Rerank compressions by path length (Filippova's method)
for cummulative_score, path in candidates:

    # Normalize path score by path length
    normalized_score = cummulative_score / len(path)

    # Print normalized score and compression
    print("%.3f: %s" % (normalized_score, " ".join([u[0] for u in path])))

# Write the word graph in the dot format
compresser.write_dot('test.dot')

# 2. Rerank compressions by keyphrases (Boudin and Morin's method)
reranker = KeyphraseReranker(sentences, candidates, lang="en")

reranked_candidates = reranker.rerank_nbest_compressions()

# Loop over the best reranked candidates
for score, path in reranked_candidates:
    # Print the best reranked candidates
    print("%.3f: %s" % (score, " ".join([u[0] for u in path])))
```
