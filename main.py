import os
import time
import cProfile
import pstats
import logging

import core.markovchain as mc
import core.sentence as sentence
from gutenberg import basic_strip as bs
import database.text_importer as ti
import database.files as store
import core.dialogue as dialogue
import knowledge.wikipedia as wiki
import knowledge.word_vectors as w2v
import knowledge.names as names
import nlp.tokenizer_stanford as tokenize

LOGDIR = "logs"
if not os.path.exists(LOGDIR):
    os.mkdir(LOGDIR)

logger = logging.getLogger(__name__)


FORMAT = '%(asctime)s %(name)12ss %(funcName)12s() %(levelname)7s: %(message)s'
logging.basicConfig(filename=LOGDIR + '/textgen.log', level=logging.DEBUG, format=FORMAT, datefmt='%m/%d/%Y %H:%M:%S')
logger.info("\n========================================== New run ==========================================")


def load_text():
    # mcW = mc.MarkovChain()
    # mcW.delete_all_in_redis_careful()

    doc = bs.get_clean_text(107)
    cache = store.files(store.Storage_type.local_dev)
    cache.write_text(doc['text'], "107.txt")
    with open("database/resources/texts/107.txt") as file_in:
        text = file_in.read()

    tokens = tokenize.tokenize(text[2000:3000])
    print(tokens['tokens'][0:50])
    print(tokens['entities'])
#     mcW.train_words(tokens['tokens'])
#     mcW.append_ner(tokens['entities'])

    generator = sentence.SentenceMaker(mc)
    s = generator.generate_sentence_tokens(["the", "man"])
    print(" ".join(s))


def dev():
    mcW = mc.MarkovChain()
    w2vec = w2v.WordVectors()
    seeds = w2vec.path("swim", 20)
    print(seeds)
    generator = sentence.SentenceMaker(mcW)
    for sd in seeds:
        sen = generator.generate_sentence_tokens([sd])
        sen = generator.polish_sentence(sen)
        print("  " + sentence.SentenceMaker.to_string(sen))
    print('')

    nm = names.NameMaker()
    speakers = [nm.random_person() for i in range(1, 4)]
    dm = dialogue.dialogue_maker([n['name'] for n in speakers], [n['pronoun'] for n in speakers], mcW, seeds)
    dlg = dm.make_dialogue()
    for s in dlg:
        print("  " + sentence.SentenceMaker.to_string(s))

    # print(wiki.wiki_random()[0:70])
    # importer = gut.TextImporter(mcW)
    # importer.get_text_from_gut(105)


if __name__ == "__main__":
    dev()
