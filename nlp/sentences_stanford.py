from nltk import sent_tokenize
import logging
logger = logging.getLogger(__name__)


# TODO:  Move behind a shared sentence-tokenizer abstract wrapper(?)

def find_sentences(text):
    """Returns list of sentences.
    Uses Stanford tokenizer then 'fixes' some false-positive splits"""
    ss = sent_tokenize(text.replace('\n', ' '))
    for idx in range(1, len(ss)):
        try:
            if ss[idx - 1][-1] == '"' and ss[idx][0].islower():
                logger.info("Merging sentence tokens: {} + {} ".format(ss[idx - 1], ss[idx]))
                ss[idx - 1] = ss[idx - 1] + " " + ss[idx]
                ss[idx] = ""
        except IndexError:
            pass
    logger.info("Found {:3d} sentences  ".format(len(ss)))
    return list(filter(None, ss))
