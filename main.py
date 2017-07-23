import core.markovchain as mc
import core.sentence as sentence
import nlp.tokenizer_stanford as tokenize
#from gutenberg import basic_strip as bs
import database.text_importer as gut
import database.files as store
import core.dialogue as dialogue
import knowledge.wikipedia as wiki
import time
import cProfile
import pstats
import logging
logger = logging.getLogger(__name__)

FORMAT = '%(asctime)s %(name)12ss %(funcName)12s() %(levelname)7s: %(message)s'
logging.basicConfig(filename='logs/textgen.log', level=logging.DEBUG, format=FORMAT, datefmt='%m/%d/%Y %H:%M:%S')
logger.info("\n========================================== New run ==========================================")


# def load_text():
#     mcW = mc.MarkovChain()
#     mcW.delete_all_in_redis_careful()

#     doc = bs.get_clean_text(103)
#     cache = store.files(store.Storage_type.local_dev)
#     cache.write_text(doc['text'],"103.txt")
#     with open("database/resources/texts/103.txt") as file_in:
#         text = file_in.read()

#     tokens = tokenize.tokenize(text[2000:20000])
#     print(tokens['tokens'][0:50])
#     print(tokens['entities'])
#     mc.train_words(tokens['tokens'])
#     mc.append_ner(tokens['entities'])

#     generator = sentence.SentenceMaker(mc)
#     s = generator.generate_sentence_tokens(["the", "man"])
#     print(" ".join(s))


def dev():
    mcW = mc.MarkovChain()
    phrase = "dog cat cat dog dog dog"
    seeds = phrase.split(" ")
    dm = dialogue.dialogue_maker(["Alice", "Bob", "Carol", "Dan"], ["she", "he", "she", "he"], mcW, seeds)
    print(dm.make_dialogue())
    # print(wiki.wiki_random()[0:70])
    # importer = gut.TextImporter(mcW)
    # importer.get_text_from_gut(105)

if __name__ == "__main__":
    dev()
    # cProfile.run('dev()','main_stats')
    # p=pstats.Stats('main_stats')

    # p.sort_stats('cumulative').print_stats(50)
