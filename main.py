import os
import time
import cProfile
import pstats
import logging
import watchtower
import core.markovchain as mc
import core.sentence as sentence

import nlp.tokenizer_stanford as tokenize
import nlp.pos as pos
import database.text_importer as gut
import database.parallelize as parallelize
from gutenberg import basic_strip as bs
import database.text_importer as ti
import database.files as store
import core.dialogue as dialogue
import knowledge.wikipedia as wiki
import knowledge.word_vectors as w2v
import knowledge.names as names

import nlp.story_grammar as story_grammar
import time
import cProfile
import pstats
import logging


LOGDIR = "logs"
if not os.path.exists(LOGDIR):
    os.mkdir(LOGDIR)

FORMAT = '%(asctime)s %(name)12s %(funcName)12s() %(levelname)7s: %(message)s'
logging.basicConfig(filename=LOGDIR + '/textgen.log', level=logging.DEBUG, format=FORMAT, datefmt='%m/%d/%Y %H:%M:%S')
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)

cloud_logger = watchtower.CloudWatchLogHandler()
cloud_logger.setLevel(logging.DEBUG)
logging.getLogger("textgen").info("Cloud logger here!")
logging.getLogger("textgen").addHandler(cloud_logger)

# parent_logger = logging.getLogger('textgen')
# parent_logger.addHandler(watchtower.CloudWatchLogHandler())


# parent_logger.info("Parent logger here!")

logger = logging.getLogger("textgen." + __name__)
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


    story_grammar.make_story(generator)

    # verbs = pos.verbs(s)
    # nouns = pos.nouns(s)
    # print(verbs)
    # print(nouns)
    # new_verb = "levitated"
    # new_noun = "hat"
    # new_s = [token if token != verbs[0] else new_verb for token in s]
    # new_s = [token if token != nouns[0] else new_noun for token in new_s]
    # print(generator.to_string(new_s))


if __name__ == "__main__":
    parallelize.dev()
