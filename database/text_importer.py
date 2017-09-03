import logging
from gutenberg import basic_strip as bs
import database.redis_store
import nlp.ner_spacy as ner
import nlp.sentences_stanford as sents
import database.files as store


logger = logging.getLogger(__name__)

# Probably best to skip these files:
# exclusions = [101, 104, 106, 114, 115, 118, 124, 127, 129, 131, 180,
#                  200, 226, 227, 229, 230, 228, 231, 232, 247, 248, 258, 266, 277, 278]


def doc_to_text(doc):
    return(str(doc.get('title', "") + "\n" + doc.get('text', "")))


class TextImporter(object):
    """Download and import text from Project Gutenberg etc."""

    def __init__(self, markovChain=None):
        # self._mc = markovChain
        self._cache = store.files(store.Storage_type.local_dev)
        self._cloud = store.files(store.Storage_type.s3)
        self._store = database.redis_store.redis_store()
        self._doc = {}

    # TODO: treat local store as a cache and only download files not already there
    def doc_from_gut(self, fileid, max_len=None):
        doc = bs.get_clean_text(fileid)
        title = doc['title']
        text = doc['text']
        if max_len:
            text=text[0:max_len]
        logger.info("Downloaded item {}: '{}' from Gutenberg:  ".format(fileid, title))
        #logger.info("Text starts: {}...".format(text[0:500]))
        self._doc = {"title": title, "text": text, "id": fileid}

    def doc_to_s3(self):
        self._cloud.write_text(doc_to_text(self._doc), str(self._doc['id']) + ".txt")

    def doc_to_cache(self):
        self._cache.write_text(doc_to_text(self._doc), str(self._doc['id']) + ".txt")

        # with open("database/resources/texts/" + filename) as file_in:
        #     text = file_in.read()

    # def tokenize(text)
    #     tokens = tokenize.tokenize(text)
    #     #logger.info("First few tokens from {}: '{}':  ".format(fileid, ",".join(tokens['tokens'][0:50])))
    #     #logger.info("First few entities from {}: '{}':  ".format(fileid, ",".join(tokens['entities'])))
    #     return tokens

    def doc_to_sentences(self):
        return(sents.find_sentences(doc_to_text(self._doc)))

    def sents_to_tokens(self, sentences):
        tokens_entities = [ner.ner(s) for s in sentences]
        return tokens_entities

    def tokens_to_s3(self, sent_tokens, ner_tokens, fileid):
        token_bucket = "dcorney.com.tokens"
        r1 = self._cloud.write_s3(sent_tokens, token_bucket, "sents_{}".format(fileid))
        r2 = self._cloud.write_s3(ner_tokens, token_bucket, "ner_{}".format(fileid))
        return((r1, r2))

    def append_title(self, title):
        self._store.add_source(title)


def dev():
    ti = TextImporter()
    ti.doc_from_gut(120)
    ti.doc_to_cache()
    ti.doc_to_s3()
    sents = ti.doc_to_sentences()
    tokens_ner = ti.sents_to_tokens(sents)
    ti.tokens_to_s3(sents, tokens_ner, 120)
