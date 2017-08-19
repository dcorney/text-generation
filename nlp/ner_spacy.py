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

    # TODO: merge adjacent tokens of same type. E.g. [<PERSON>, <PERSON>] -> [<PERSON>]. I.e. just delete second one of each pair.
    entities = [{normalize_types.get(e.label_, e.label_): e.text} for e in doc.ents if normalize_types.get(e.label_, e.label_) in types]
    tokens = [normalize_types.get(t.ent_type_, t.text) for t in doc]
    return {"tokens": tokens, "entities": entities}


def dev():
    text = "What the BBC thinks about London  and    Mrs Jones."
    print(ner(text))
