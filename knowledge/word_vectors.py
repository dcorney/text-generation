from gensim.models import Word2Vec
import random
from knowledge.synonymizer import Synonymizer
from itertools import chain
import utils


class WordVectors(Synonymizer):
    """Generate synonyms for a word using Wordnet thesaurus"""

    # TODO: a) retrain this on novels; b) move to S3 & download iff missing
    def __init__(self):
        utils.s3_download(utils.S3_RESOURCE_BUCKET, 'signal_w2v.model', 'resources/signal_w2v.model', aws_profile='default')
        self.model_signal = Word2Vec.load('resources/signal_w2v.model')

    def sim(self, word):
        try:
            related = self.model_signal.most_similar(positive=[word])
            return([w for w, s in related])
        except KeyError:
            return([word])

    def synonym(self, word):
        return(self.sim(word)[0])

    def synonyms(self, seeds, n=10):
        """Return a list of n words """
        # take from each in turn, adding to a list of lists (one per seed), then merge into one list
        # Loop through lists multiple times if needed to produce n items.
        seed_terms = [self.sim(s) for s in seeds]
        terms = []
        longest = 0
        for i in range(0, len(seeds)):
            terms.append([])
            if len(seed_terms[i]) > longest:
                longest = len(seed_terms[i])
        total = 0
        j = 0
        while total < n:
            total = 0
            for i in range(0, len(seeds)):
                if len(seed_terms[i]) > j:
                    terms[i].append(seed_terms[i][j])
                total += len(terms[i])
            j += 1
            if j > longest:
                j = 0  # Loop back to point to start of all seed_term lists
        final_terms = list(chain.from_iterable(terms))
        return(final_terms[0:n])

    def path(self, root, n=10, stepsize=3):
        """Return a list of terms by repeatedly finding the most-similar terms
        from a word2vec model. Stepsize specifies how many terms to return
        from each node in the chain."""
        seq = []
        seq.append(root)
        while len(seq) < n:
            next = self.sim(seq[-1])
            random.shuffle(next)
            maxToAdd = stepsize
            for j in next:
                if j not in seq:
                    seq.append(j)
                    maxToAdd -= 1
                    if maxToAdd <= 0:
                        break
        return(seq[0:n])


def dev():
    wv = WordVectors()
    #print(wv.synonyms(["man", "planet"], 25))
    print(wv.path("man",12))
