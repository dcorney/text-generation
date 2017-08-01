from nltk.corpus import wordnet
import random
from knowledge.synonymizer import Synonymizer
import logging

logger = logging.getLogger(__name__)


class WordNet(Synonymizer):
    """Generate synonyms for a word using Wordnet thesaurus"""

    def synonym(self, word):
        all_synsets = wordnet.synsets(word)
        if not all_synsets:
            morphed = wordnet.morphy(word)
            logger.info("Word '{}' not found in wordnet; morphing to '{}'".format(word, morphed))
            if morphed is None:
                return word
            if morphed:
                all_synsets = wordnet.synsets(morphed)
            if not all_synsets:
                return word

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

    def synonyms(self, init_list, n=10):
        "Take a list of words and return a list of n words, including\
        repetitions and synonyms etc. of the originals"
        if isinstance(init_list, str):
            init_list = init_list.split()
        seeds = []
        for i in range(0, n):
            idx = i * len(init_list) // n
            term = init_list[idx]
            if random.random() < 0.75:  # sometimes keep the original word
                term = self.synonym(term)
            seeds.append(term)
        return(seeds)

    def path(self, root, n=10, stepsize=3):
        """Return a list of terms by repeatedly finding the most-similar terms
        from a word2vec model. Stepsize specifies how many terms to return
        from each node in the chain."""
        seq = []
        seq.append(root)
        while len(seq) < n:
            next = self.synonyms([seq[-1]], stepsize)
            random.shuffle(next)
            maxToAdd = stepsize
            added_something = False
            for j in next:
                if j not in seq:
                    seq.append(j)
                    added_something = True
                    maxToAdd -= 1
                    if maxToAdd <= 0:
                        break
            if added_something is False:
                seq.append(root)
        return(seq[0:n])


def dev():
    wn = WordNet()
    print(wn.synonyms(["denial", "tabular", "dog"], 20))
    print(wn.path("dog", 200))
