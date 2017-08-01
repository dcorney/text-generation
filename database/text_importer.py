import logging
from gutenberg import basic_strip as bs
import database.redis_store
import nlp.tokenizer_stanford as tokenize
import database.files as store


logger = logging.getLogger(__name__)

#Probably best to skip these files:
 # exclusions = [101, 104, 106, 114, 115, 118, 124, 127, 129, 131, 180,
 #                  200, 226, 227, 229, 230, 228, 231, 232, 247, 248, 258, 266, 277, 278]


class TextImporter(object):
    """Download and import text from Project Gutenberg etc."""

    def __init__(self, markovChain):
        self._mc = markovChain
        self._cache = store.files(store.Storage_type.local_dev)
        self._store = database.redis_store.redis_store()

    def tokenize_from_gut(self, fileid):
        filename = str(fileid) + ".txt"
        doc = bs.get_clean_text(fileid)
        title = doc['title']
        text = doc['text']
        logger.info("Downloaded item {}: '{}' from Gutenberg; saving as '{}':  ".format(fileid, title, filename))
        logger.info("Text starts: {}...".format(text[0:500]))
        self._cache.write_text(text, filename)
        # with open("database/resources/texts/" + filename) as file_in:
        #     text = file_in.read()

        tokens = tokenize.tokenize(text)
        logger.info("First few tokens from {}: '{}':  ".format(fileid, ",".join(tokens['tokens'][0:50])))
        logger.info("First few entities from {}: '{}':  ".format(fileid, ",".join(tokens['entities'])))
        return tokens
        
    def tokens_to_s3(self, tokens, fileid):
        filename = "gut" + str(fileid)
        s3 = store.files(store.Storage_type.s3)
        s3.write_text(tokens, filename)



    def tokens_to_mc(self, tokens):
        self._mc.train_words(tokens['tokens'])
        self._mc.append_ner(tokens['entities'])
        self.append_title("Gutenburg " + str(fileid) + " " + title + "|" + str(len(tokens['tokens'])) + "|" + str(len(tokens['entities'])))
        logger.info("Imported {} tokens into markovchain".format(len(tokens['tokens'])))

    # TODO: treat local store as a cache and only download files not already there
    def get_text_from_gut(self, fileid):
        
        # generator = sentence.SentenceMaker(mc)
        # s = generator.generate_sentence_tokens(["the", "man"])
        # print(" ".join(s))
        pass

    def append_title(self, title):
        self._store.add_source(title)

def dev():
    import core.markovchain as mc
    mcW = mc.MarkovChain()
    ti = TextImporter(mcW)
    tokens = ti.tokenize_from_gut(105)
    ti.tokens_to_s3(tokens, 105)
