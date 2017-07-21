from nltk import word_tokenize, sent_tokenize
from nltk.tag import StanfordNERTagger
from utils import START_TOKEN, END_TOKEN
import logging
logger = logging.getLogger(__name__)

# Use NER to replace PEOPLE, LOCATION, ORGANISATION tags with special tokens
# Then replace those with suitable tokens from another list
# Change tokenize() to return list of tokens + lists of instances of each type
# E.g. {tokens: ["PERSON" "said" to "PERSON" "'" "Hello" "there" "PERSON"] ,
#       people: ["John" "Mary" "Mary"], locations: [], organisations :[]}

st = StanfordNERTagger("resources/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz",
                       "resources/stanford-ner-2014-06-16/stanford-ner-3.4.jar")


def ner_tags(tokens):
    ner_tags = st.tag(tokens)
    tagged_tokens = [token if ner_type == 'O' else "<" +
                     ner_type + ">" for [token, ner_type] in ner_tags]
    trimmed_tokens = []
    for idx, tag in enumerate(tagged_tokens):
        if idx == 0 or tag != tagged_tokens[idx - 1]:
            trimmed_tokens.append(tag)
    return trimmed_tokens


def process_ner_tags(ner_tags):
    "Merge adjacent tags of the same type \
    (e.g. 'south' + 'africa' -> 'south africa')"
    merged_tags = []
    merged_token = ["", ""]
    for idx, (token, ner_type) in enumerate(ner_tags):
        if idx == 0:
            merged_token = [token, ner_type]
        else:
            if ner_type == "O":
                merged_tags.append(merged_token)
                merged_token = [token, ner_type]
            else:
                if ner_type == ner_tags[idx - 1][1]:
                    merged_token[0] += " " + token
                    merged_token[1] = ner_type
                else:
                    merged_tags.append(merged_token)
                    merged_token = [token, ner_type]
    merged_tags.append(merged_token)
    return(merged_tags)


def tokens_to_types(merged_tags):
    examples = {}  # {"ORGANIZATION": [], "PERSON": [], "LOCATION": []}
    tokens = []
    for [token, ner_type] in merged_tags:
        if ner_type == "O":
            tokens.append(token)
        else:
            ee = examples.get(ner_type, [])
            ee.append(token)
            examples[ner_type]=ee
            tokens.append("<" + ner_type + ">")
    return {'tokens': tokens, 'entities': examples}


def tokenize_sentence(s):
    tk_list = word_tokenize(s)
    ner_tags = st.tag(tk_list)
    merged_tags = process_ner_tags(ner_tags)
    tokens_entities = tokens_to_types(merged_tags)
    tokens_entities['tokens'].insert(0, START_TOKEN)
    tokens_entities['tokens'].append(END_TOKEN)
    logger.info("Sentence NEs: {}".format(tokens_entities['entities']))
    logger.info("Sentence tokens: {}".format(tokens_entities['tokens']))
    return tokens_entities


def find_sentences(text):
    ss = sent_tokenize(text)
    for idx in range(1, len(ss)):
        if ss[idx - 1][-1] == '"' and ss[idx][0].islower():
            logger.info("Merging sentence tokens: {} + {} ".format(ss[idx - 1], ss[idx]))
            ss[idx - 1] = ss[idx - 1] + " " + ss[idx]
            ss[idx] = ""
    return list(filter(None, ss))


# TODO: move string labels into vars (org="ORGANIZATION" etc)
def tokenize(text):
    """
    Split text into sentences; then split sentences into tokens.
    Also tags entities and returns list of surface forms.
    """
    sents = find_sentences(text)
    logger.info("Found {:3d} sentences  ".format(len(sents)))
    flattened_tokens = []
    merged_entities = {"ORGANIZATION": [], "PERSON": [], "LOCATION": []}
    for s in sents:
        tokens_entities = tokenize_sentence(s)
        tokens = tokens_entities['tokens']
        entities = tokens_entities['entities']
        flattened_tokens += (tokens)
        merged_entities['ORGANIZATION'] += entities.get('ORGANIZATION', [])
        merged_entities['PERSON'] += entities.get('PERSON', [])
        merged_entities['LOCATION'] += entities.get('LOCATION', [])
    return {'tokens': flattened_tokens, 'entities': merged_entities}


def dev():
    text = "This is the first sentence. This second sentence is about Paris. The third sentence mentions Mr. John Smith, O.B.E."
    ts = tokenize(text)
    print(ts)
