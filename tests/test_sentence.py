from context import sentence as sent
from context import core as core
import pytest

def test_generate():
    mc = core.markovchain.MarkovChain()
    ss = sent.SentenceMaker(mc)
    tokens = ss.generate_sentence_tokens(["this", "is"])
    sent_str = ss.to_string(tokens)
    assert isinstance(tokens, list)
    assert isinstance(sent_str, str)

    tokens = ss.generate_sentence_tokens(["UnlikelyTokens", "ForASeedQqqqq"])
    sent_str = ss.to_string(tokens)
    assert isinstance(tokens, list)
    assert isinstance(sent_str, str)


    with pytest.raises(AssertionError):
        tokens = ss.generate_sentence_tokens("fred")

    with pytest.raises(AssertionError):
        tokens = ss.generate_sentence_tokens([0,1,2])
