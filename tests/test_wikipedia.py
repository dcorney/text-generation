from context import wiki as wikipedia


def test_random_bits():
    test_strings = ["dog", "Martin Luther", "zxqpolrn_fake"]
    for t in test_strings:
        text = wikipedia.wiki_text(t)
        assert isinstance(text, str)
        print("String '{}'' returns '{}...'".format(t, text[0:70]))


if __name__ == '__main__':
    test_random_bits()
