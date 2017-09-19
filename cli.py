import argparse
import core.sentence as sentence
import core.markovchain as mc
import core.paragraphs as paras
import nlp.story_grammar as story_grammar


def make_sentences(n=1):
    mcW = mc.MarkovChain()
    generator = sentence.SentenceMaker(mcW)
    s = generator.generate_sentence_tokens(["the"])
    p = paras.seq_to_para(s[0:n], mcW)
    for sent in p:
        print(generator.to_string(generator.polish_sentence(sent)))


def make_story():
    mcW = mc.MarkovChain()
    generator = sentence.SentenceMaker(mcW)
    story_grammar.make_story(generator)


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("--make", action='store', type=int, help="Make & show n sentences")
    parser.add_argument("--story", action='store_true', help="Make & show a story!")

    args = parser.parse_args()
    if args.make:
        make_sentences(args.make)
        exit(0)
    if args.story:
        make_story()
        exit(0)

