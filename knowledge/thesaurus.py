from nltk.corpus import wordnet as wn
import random

# See http://www.nltk.org/howto/wordnet.html
# e.g. synset.defintion()


def synonym(word):
    all_synsets = wn.synsets(word)
    if not all_synsets:
        morphed = wn.morphy(word)
        print("Word '{}' not found in wordnet; morphing to '{}'".format(word, morphed))
        if morphed:
            all_synsets = wn.synsets(morphed)
        if not all_synsets:
            return word
    # synset = all_synsets[0]
    synset = random.choice(all_synsets)
    terms = [t for h in synset.hyponyms() for t in h.lemmas()]
    if terms:
        lemma = random.choice(terms)
        synonym = lemma.name()
    else:
        terms = synset.lemma_names()
        if not terms:
            return word
        synonym = random.choice(terms)
    return(synonym.replace("_", " "))


def expand_seeds(init_list, n=10):
    "Take a list of words and return a list of n words, including\
    repetitions and synonyms etc. of the originals"
    if isinstance(init_list, str):
        init_list = init_list.split()
    seeds = []
    for i in range(0, n):
        idx = i * len(init_list) // n
        term = init_list[idx]
        if random.random() < 0.75:  # sometimes use the original word
            term = synonym(term)
        seeds.append(term)
    return(seeds)


def dev():
    print(expand_seeds(["denial", "tabular", "dog"], 20))
