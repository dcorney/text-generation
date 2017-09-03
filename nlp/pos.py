from spacy.en import English
from nltk.corpus import stopwords
import knowledge.wikipedia as wikipedia

nlp = English()
stopwords = stopwords.words('english')
stopwords.append("go")
good_tags = ["VBG", "VBP", "VBN", "VBZ", "NN", "NNS", "JJ", "JJS"]


def all_tags(tokens):
    """Return POS tags, lemmas for each token"""
    doc = nlp(" ".join(tokens))
    return(doc)


def meaning_words(tokens, lemmas=False):
    """Filters list of tokens to return just verbs, nouns, adjectives that
    are also not stopwords"""
    doc = all_tags(tokens)
    tokens = [token for token in doc if token.lemma_.lower() not in stopwords
              and token.tag_ in good_tags]
    if lemmas is False:
        w = [t.text for t in tokens]
    else:
        w = [t.lemma_ for t in tokens]
    return(w)


def verbs(tokens):
    """Return text of each verb"""
    verbs = [t.text for t in all_tags(tokens) if t.tag_ in ["VBG","VBP","VBN","VBZ"]]
    return(verbs)


def nouns(tokens):
    """Return text of each verb"""
    nouns = [t.text for t in all_tags(tokens) if t.tag_ in ["NN","NNS"]]
    return(nouns)


def dev(seed, lemmas=False):
    t = wikipedia.wiki_text(seed)
    w = meaning_words(t.split(), lemmas)
    print(w)
