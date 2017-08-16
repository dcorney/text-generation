from spacy.en import English

nlp = English()

# TODO:  Move behind a shared NER abstract wrapper(?)

"""Map to consistent names """
normalize_types = {"ORG": "ORGANIZATION",
                   "GPE": "LOCATION"}


def ner(text, types=["PERSON", "ORGANIZATION", "LOCATION"]):
    """Finds named entities in given text string. Only returns
    requested types. """
    doc = nlp(" ".join(text.split()))

    #change this! Should process every word e.g
    # for word in doc: 
    # then if it's an entity, add it to the appropriate type list and add a <TYPE> token to the token list
    # else add the token string itself to the token list
    # And return a map of {"tokens":token_list, "person":person_list,.. etc}
    
    sp_all = [{normalize_types.get(e.label_, e.label_): e.text} for e in doc.ents if normalize_types.get(e.label_, e.label_) in types]

    return sp_all


def dev():
    text = "What the BBC thinks about London and Mrs Jones."
    print(ner(text))
