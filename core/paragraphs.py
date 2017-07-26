import core.sentence as sentence
import nltk
from nltk.tokenize import RegexpTokenizer
import knowledge.wikipedia as wikipedia
import knowledge.thesaurus as thesaurus
import random
import logging

logger = logging.getLogger(__name__)


# TODO: ideally, want to deal with NEs here too: replace with tags when making seed phrase.
def phrase_from_sentence(sentence, n):
    """Pick a random sequence of words from a sentence."""
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(sentence)
    start = random.randint(0, max(0, (len(tokens) - n)))
    phrase_tokens = tokens[start:start + n]
    return(" ".join(phrase_tokens))


def phrases_from_wiki(query, phrase_length, max_phrases=50):
    """Get text from wikipedia; then for each sentence, return a sequence of words."""
    text = wikipedia.wiki_text(query)
    sents = nltk.sent_tokenize(text)
    all_phrases = [phrase_from_sentence(s, phrase_length) for s in sents]
    return (all_phrases[0:min(max_phrases, len(all_phrases) - 1)])


def seq_to_para(seq, mc):
    """Takes a sequence of seed phrases & returns one sentence for each, as a list of lists of words"""
    sm = sentence.SentenceMaker(mc)
    para = []
    for seed in seq:
        seed_tokens = seed.split()
        tokens = sm.generate_sentence_tokens(seed_tokens)
        para.append(tokens)  # ss.to_string(tokens) + "  "
    return para


def sentences_from_thesaurus(seeds, mc, n=10):
    new_seeds = thesaurus.expand_seeds(seeds, n)
    para = seq_to_para(new_seeds, mc)
    return(para)


def dev():
    import core.markovchain as mc
    mcW = mc.MarkovChain()
    sm = sentence.SentenceMaker(mcW)
    ss=sentences_from_thesaurus(["cat","anger","sorry","cat"],mcW)
    for s in ss:
        sent = sm.polish_sentence(s)
        print("   " + sm.to_string(sent))


# # Do we still need this? If so, need to add back in scoring fn. to Sentence class, based on length etc.
# def scored_sentence(seed, mc, target_length=None):
#     ss = sentence.Sentence(mc)
#     seed_tokens = seed.split()
#     score = -1
#     attempts = 5
#     while score < 0 and attempts > 0:
#         s = ss.generate_sentence(seed_tokens, target_length)
#         score = s._score
#         attempts -= 1
#     return s


# def phrases_to_para(phrases, mc):
#     para = ""
#     for phrase in phrases:
#         seed = phrase.split(" ")
#         # tokens = mc.generate_sentence(seed)
#         # s = Sentence.Sentence(tokens)
#         s = scored_sentence(seed, mc)
#         para += s.get_text() + "  "
#     return para

# defn text->seq - takes a block of text and produces a sequence of seeds
# of a given model size

# defn wiki->text (different module?)
