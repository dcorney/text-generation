import database.redis_store
import utils
from numpy import cumsum, sum, searchsorted
from numpy.random import rand
import logging

logger = logging.getLogger(__name__)


class MarkovChain(object):
    """Train bi-directional Markov chain over sequences of tokens.
    Then generate new sequences."""

    def __init__(self, order=3):
        self._order = order
        self._store = database.redis_store.redis_store()
        self._symbols = []
        self._source_field = "SOURCE_LIST"

    def delete_all_in_redis_careful(self):
        self._store.delete_all_in_redis_be_careful()

    def get_order(self):
        return self._order

    def add_sentence(self, sentence, weight=1):
        """Takes a string as a sentence, splits on white space, adds start & end token, then udpates model"""
        tokens = sentence.split()
        tokens.insert(0, utils.START_TOKEN)
        tokens.append(utils.END_TOKEN)
        self.train_words(tokens, weight)

    def train_words(self, tokens, weight=1):
        """Take list of tokens and update model."""
        for idx in range(len(tokens)):
            start = max(0, idx - self._order)
            end = idx
            for sub_idx in range(start, end):
                node_from = '|'.join(tokens[sub_idx:end]) + ":fwd"
                node_to = str(tokens[idx])
                #logger.info("Adding link from '%s' fwd-to '%s':  ", node_from, node_to)
                self._store.update_weight(node_from, node_to, weight)
            start = idx + 1
            end = min(idx + self._order + 1, len(tokens))
            for sub_idx in range(start + 1, end + 1):
                node_from = '|'.join(tokens[start:sub_idx]) + ":back"
                node_to = str(tokens[idx])
                #logger.info("Adding link from '%s' back-to '%s':  ", node_from, node_to)
                self._store.update_weight(node_from, node_to, weight)

    def append_ner(self, entities):
        self._store.append_ner(entities)

    def unappend_ner(self, entities):
        self._store.unappend_ner(entities)

    def get_probs(self, tokens, direction='forward'):
        node_from = '|'.join(tokens)
        if direction == 'reverse':
            probs = self._store.get_weights(node_from + ":back")
        else:
            probs = self._store.get_weights(node_from + ":fwd")
        if (len(probs) == 0):
            if len(tokens) == 0:
                # TODO: should be :back half the time:
                while (len(probs) == 0):
                    # TODO: not sure why this bit is needed... how can a random-entry have no probs?
                    e = self._store.random_entry()
                    probs = self._store.get_weights('|'.join(e) + ":fwd")
            else:
                if direction == 'reverse':
                    sub_seq = tokens[0:-1]
                else:
                    sub_seq = tokens[1:]
                probs = self.get_probs(sub_seq, direction)
        logger.info("Probs from '%s' : %d ", node_from, len(probs))
        return probs

    def predict(self, sequence, direction='forward', terminal_boost=1):
        """
        Takes in input a list of words and predicts the next word.
        Uses variable bias towards (or away from) sentence-termination markers.
        """
        def terminal_token(t):
            word = t.decode('UTF-8')
            if word == "<sentence_start>" or word == "<sentence_end":
                return terminal_boost
            else:
                return 1
        probs = self.get_probs(sequence, direction)
        weights = [int(w) * terminal_token(word) for word, w in probs.items()]
        idx = searchsorted(cumsum(weights), rand() * sum(weights))
        logger.debug("Predicting from '%s' with %d probs", str(sequence), len(probs))
        return list(probs.keys())[idx].decode("utf-8")

    def random_entry(self):
        "Make sure random entry is not a special token (e.g. sentence-start)"
        return self._store.random_entry()

    def random_entity(self, ner_type):
        """Returns random entity of specified type"""
        return self._store.random_entity(ner_type)
