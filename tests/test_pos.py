from context import pos as pos


text = "This is a short sentence about a dog."
tokens = text.split(" ")

def test_regex():

    tags = pos.all_tags(tokens)
    print(tags)
    # assert 1 ==0
    assert isinstance(tokens, list)
    assert isinstance(tokens[0], str)

