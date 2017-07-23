from context import core as core

mc = core.markovchain.MarkovChain()


def test_random_bits():
    test_seq = ["this", "is"]
    probs = mc.get_probs(test_seq)
    print("Sequence '%s' has %d out-links" % (",".join(test_seq), len(probs)))
    assert isinstance(probs, dict)

    next_word = mc.predict(test_seq, direction='forward')
    print("Sequence '%s' may be followed by %s " % (",".join(test_seq), next_word))
    assert isinstance(next_word, str)

    next_item = mc.random_entry()
    print(type(next_item))
    assert isinstance(next_item, list)


if __name__ == '__main__':
    test_random_bits()
