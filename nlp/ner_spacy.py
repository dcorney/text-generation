from spacy.en import English

nlp = English()

# TODO:  Move behind a shared NER abstract wrapper(?)

"""Map to consistent names """
normalize_types = {"ORG": "<ORGANIZATION>",
                   "GPE": "<LOCATION>",
                   "PERSON": "<PERSON>"}


def ner(text, types=["<PERSON>", "<ORGANIZATION>", "<LOCATION>"]):
    """Finds named entities in given text string. Only returns
    requested types (and the text of other tokens). """
    doc = nlp(" ".join(text.split()))

    # merge adjacent tokens of same type. E.g. [<PERSON>, <PERSON>] -> [<PERSON>]. I.e. just delete second one of each pair.
    entities = [{normalize_types.get(e.label_, e.label_): e.text} for e in doc.ents if normalize_types.get(e.label_, e.label_) in types]
    tokens = [normalize_types.get(t.ent_type_, t.text) for t in doc]
    tokens_filtered = [token for idx, token in enumerate(tokens)
                       if idx == 0 or (token != tokens[idx - 1] and token[0] == "<")]
    return {"tokens": tokens_filtered, "entities": entities}


def dev():
    text = "What the BBC thinks about London  and  Barry Jones."
    print(ner(text))
