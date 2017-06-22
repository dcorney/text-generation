from context import markovchain

mc = markovchain.markovchain.MarkovChain()


def test_random_entry():
    next_item = mc.random_entry()
    print(type(next_item))
    assert isinstance(next_item, list)


if __name__ == '__main__':
    test_random_entry()
