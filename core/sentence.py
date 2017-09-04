import sys
import utils
import re
import logging

logger = logging.getLogger("textgen." + __name__)


class SentenceMaker(object):
    """Build & process a sentence as a sequence of words/tokens."""
    def __init__(self, markovChain):
        self._markovChain = markovChain

    def generate_sentence_tokens(self, start, target_length=None):
            """Uses seed token-list as 'middle' of new sentence, growing it
            until it starts & ends with 'end' tokens.
            Target length parameter used to bias word-count; if 'none', then no bias is used."""
            assert isinstance(start, list)
            assert isinstance(start[0], str)
            mc_order = self._markovChain.get_order()
            if target_length is None:
                attempts = 1  # just return first sentence generated
                target_length = sys.maxsize  # don't limit length
            else:
                attempts = 3  # generate up to this many sentences and return 'best'
            best_err = sys.maxsize
            sentence_length = sys.maxsize
            best_sentence = []
            while attempts > 0:
                result = list(start)  # make a copy of start so we don't mutate it
                terminal_boost = 1  # initial boost to 'encourage' termination of Markov process
                # Build sentence:
                while result[-1] != utils.END_TOKEN:
                    if len(result) > (target_length * 0.75):
                        terminal_boost += 1
                    new = self._markovChain.predict(result[-mc_order:], 'forward', terminal_boost)
                    logger.info("Generate fwd from '%s' to '%s':  ", str(result[0:mc_order]), new)
                    result.append(new)
                while result[0] != utils.START_TOKEN:
                    if len(result) > (target_length * 0.85):
                        terminal_boost += 1
                    new = self._markovChain.predict(result[0:mc_order], 'reverse', terminal_boost)
                    logger.info("Generate reverse from '{}' to '{}':  ".format(str(result[0:mc_order]), new))
                    result.insert(0, new)
                # Evaluate sentence
                sentence_length = len(result)
                err_len = abs(target_length - sentence_length)
                if err_len < best_err:
                    best_err = err_len
                    best_sentence = result
                attempts -= 1
                logger.info("Attempts %d   Len %d   Best-err %d ", attempts, sentence_length, best_err)
            # best_sentence = self.polish_sentence(best_sentence)
            return best_sentence

    def concrete_entities(self, token):
        """Replace entity-place-holders with random entity of appropriate type"""
        if token[1:-1] == utils.ner_loc or token[1:-1] == utils.ner_org or token[1:-1] == utils.ner_per:
            return(self._markovChain.random_entity(token[1:-1]))
        else:
            return token

    def polish_sentence(self, sentence):
        polished = [self.concrete_entities(t) for t in sentence]
        first_word = polished[1]
        polished[1] = first_word.capitalize()
        return polished

    @staticmethod
    def to_string(sentence):
        """Convert sentence tokens into a sentence string and remove excess spaces"""
        s = " ".join(sentence[1:-1])
        s = re.sub(r' ([,;]) ', r'\1 ', s)
        s = re.sub(r' (\'s|\'S) ', r'\1 ', s)
        if s[-2:] == " .":
            s = s[0:-2] + "."
        return(s)
