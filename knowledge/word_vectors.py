from gensim.models import Word2Vec
import random

model_signal = Word2Vec.load('resources/signal_w2v.model')


def sim(word):
    related = model_signal.most_similar(positive=[word])
    print(related)
    return([w for w, s in related])


def make_sequence(root, n=10, stepsize=3):
    seq = []
    seq.append(root)
    # for i in range(1, n):
    while len(seq) < n:
        next = sim(seq[-1])
        random.shuffle(next)
        maxToAdd = stepsize
        for j in next:
            if j not in seq:
                seq.append(j)
                maxToAdd-=1
                if maxToAdd<=0:
                    break

    return(seq)
