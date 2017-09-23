import argparse
import core.sentence as sentence
import core.markovchain as mc
import core.paragraphs as paras
import nlp.story_grammar as story_grammar
import knowledge.names as names
import core.dialogue as dialogue

mcW = mc.MarkovChain()
generator = sentence.SentenceMaker(mcW)


def make_seeds(seeds, max=5):
    if seeds is None:
        seeds = generator.generate_sentence_tokens(["the"])  # Make a random sentence of seeds
        seeds = seeds[0:max]
    return seeds


def make_sentences(n, seeds=None):
    seeds = make_seeds(seeds)
    # if seeds is None:
    #     seeds = generator.generate_sentence_tokens(["the"]) # Make a random sentence of seeds
    if isinstance(seeds, str):
        seeds = seeds.split()
    p = paras.seq_to_para(seeds[0:n], mcW)
    for sent in p:
        print(generator.to_string(generator.polish_sentence(sent)))


def make_story():
    story_grammar.make_story(generator)


def make_dialogue(nspeakers=4, seeds=None):
    seeds = make_seeds(seeds, 8)
    nm = names.NameMaker()
    speakers = [nm.random_person() for i in range(1, nspeakers)]
    dm = dialogue.dialogue_maker([n['name'] for n in speakers], [n['pronoun'] for n in speakers], mcW)
    dlg = dm.make_dialogue(seeds)
    for s in dlg:
        print(generator.to_string(generator.polish_sentence(s)))


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("--make", action='store', type=int, help="Make & show n sentences")
    parser.add_argument("--story", action='store_true', help="Make & show a story!")
    parser.add_argument("--seed", action='store', type=str, help="Seed word/phrase for generation")
    parser.add_argument("--dialogue", action='store', type=int, help="Dialogue between n people")
    # TODO: add args:
    
    # pre-process numbered texts from Gutenburg
    # import pre-processed numbered texts (from S3)
    # test synonyms


    args = parser.parse_args()
    if args.make:
        make_sentences(args.make, args.seed)
        exit(0)
    if args.story:
        make_story()
        exit(0)
    if args.dialogue:
        make_dialogue(args.dialogue, args.seed)
        exit(0)
