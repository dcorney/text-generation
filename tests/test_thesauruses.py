from context import wordnet as wordnet
from context import word_vectors as w2v


def test_synonyms():
    wn = wordnet.WordNet()
    wv = w2v.WordVectors()
    assert isinstance(wn.synonym("dog"), str)
    assert isinstance(wv.synonym("dog"), str)

    assert isinstance(wn.synonym("znorkqq"), str)
    assert isinstance(wv.synonym("znorkqq"), str)

    assert isinstance(wn.synonyms(["dog", "znorkqq"])[0], str)
    assert isinstance(wv.synonyms(["dog", "znorkqq"])[0], str)

    n = 11
    p1 = wn.path("dog", n)
    p2 = wv.path("dog", n)
    assert isinstance(p1[0], str)
    assert isinstance(p2[0], str)
    assert len(p1) == n
    assert len(p2) == n
