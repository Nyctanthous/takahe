"""
Collection of utility functions for users of Takahe3
"""
EN_PUNCTUATION = frozenset([".", "!", "?", ";"])

def tag_text_part_of_speech(raw_text, punctuation=EN_PUNCTUATION):
    """
    Convert ordinary strings containing sentences into Takahe-ready format
    """
    try:
        import nltk
    except ImportError as e:
        raise ImportError(
            "NLTK is required for tagging functionality but is not installed"
        ) from e

    text = nltk.pos_tag(nltk.word_tokenize(raw_text))

    all_tokenized_sentences = [[]]
    for word, part_of_speech in text:
        if word in punctuation:
            all_tokenized_sentences[-1].append(f"{word}/PUNCT")
            all_tokenized_sentences.append([])
        else:
            all_tokenized_sentences[-1].append(f"{word}/{part_of_speech}")

    return [
        " ".join(tokenized_sentence)
        for tokenized_sentence in all_tokenized_sentences
        if tokenized_sentence
    ]
