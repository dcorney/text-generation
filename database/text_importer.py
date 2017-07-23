from gutenberg import basic_strip as bs
import database.redis_store
import nlp.tokenizer_stanford as tokenize
import database.files as store
import logging

logger = logging.getLogger(__name__)


class TextImporter(object):
    """Download and import text from Project Gutenberg etc."""

    def __init__(self, markovChain):
        self._mc = markovChain
        self._cache = store.files(store.Storage_type.local_dev)
        self._store = database.redis_store.redis_store()

    # TODO: treat local store as a cache and only download files not already there
    def get_text_from_gut(self, fileid):
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
        self._mc.train_words(tokens['tokens'])
        self._mc.append_ner(tokens['entities'])
        self.append_title("Gutenburg " + str(fileid) + " " + title + "|" + str(len(tokens['tokens'])) + "|" + str(len(tokens['entities'])))

        # generator = sentence.SentenceMaker(mc)
        # s = generator.generate_sentence_tokens(["the", "man"])
        # print(" ".join(s))

    def append_title(self, title):
        self._store.add_source(title)
