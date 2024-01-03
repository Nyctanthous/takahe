#!/usr/bin/python3
# -*- coding: utf-8 -*-

from takahe3.takahe import WordGraph, KeyphraseReranker

sentences = [
    "The/DT wife/NN of/IN a/DT former/JJ U.S./NNP president/NN \
              Bill/NNP Clinton/NNP Hillary/NNP Clinton/NNP visited/VBD \
              China/NNP last/JJ Monday/NNP ./PUNCT",
    "Hillary/NNP Clinton/NNP \
              wanted/VBD to/TO visit/VB China/NNP last/JJ month/NN but/CC \
              postponed/VBD her/PRP$ plans/NNS till/IN Monday/NNP last/JJ \
              week/NN ./PUNCT",
    "Hillary/NNP Clinton/NNP paid/VBD a/DT \
              visit/NN to/TO the/DT People/NNP Republic/NNP of/IN China/NNP \
              on/IN Monday/NNP ./PUNCT",
    "Last/JJ week/NN the/DT \
              Secretary/NNP of/IN State/NNP Ms./NNP Clinton/NNP visited/VBD \
              Chinese/JJ officials/NNS ./PUNCT",
]

# Create a word graph from the set of sentences with parameters :
# - minimal number of words in the compression : 6
# - language of the input sentences : en (english)
# - POS tag for punctuation marks : PUNCT
compressor = WordGraph(sentences, nb_words=6, lang="en", punct_tag="PUNCT")

# Get the 50 best paths
candidates = compressor.get_compression(50)

# 1. Re-rank compressions by path length (Filippova's method)
results = {
    # Normalize path score by path length
    cumulative_score / len(path): " ".join([u[0] for u in path])
    for cumulative_score, path in candidates
}
for score, path in sorted(results.items()):
    # Print the best re-ranked candidates
    print(f"{score:.3}: {path}")

# Write the word graph in the dot format
compressor.write_dot("test.dot")

# 2. Re-rank compressions by keyphrases (Boudin and Morin's method)
reranker = KeyphraseReranker(sentences, candidates, lang="en")

reranked_candidates = reranker.rerank_nbest_compressions()

# Loop over the best re-ranked candidates
for score, path in reranked_candidates:
    # Print the best re-ranked candidates
    print(f"{score:.3}: {' '.join([u[0] for u in path])}")
