import numpy as np
from numpy import cumsum, sum, searchsorted
from numpy.random import rand
import math
import utils
import core.sentence as sentence
import core.markovchain as mc
import logging

logger = logging.getLogger(__name__)

# Dialogue making class. Need to review where to return a string, where to return a list of tokens, etc.
# setters: list of speakers, pronouns, priors etc.
# random transitions
# Internal: build list of structures:
#     e.g.{:speaker_name "Alice", :speaker_pronoun "she", :speaker_str "she", :speech_verb "said", :position "end"}
# Then end with fn that maps that out to a suitable string
#     e.g. "<SPEECH>, she said."
# External bit then replaces <SPEECH> with a markov-chain-generated sentence (or several).


class dialogue_maker(object):
    """Class to handle creating dialogue based on a list of speakers and a sentence generator."""
    def __init__(self, names, pronouns, mc):
        self.speakers = [{"name": n, "pronoun": p} for n, p in list(zip(names, pronouns))]
        self._transitions = self.make_transition_probs()
        self._speech_acts = ["said", "whispered", "shouted", "cried"]
        self._acts_transitions = [25, 2, 2, 2]
        self.mc = mc
        # self.seeds = seeds
        self.target_len = np.random.randint(5, 50, size=len(names))  # rough words per sentence

    def make_transition_probs(self):
        """Make transition matrix between speakers, with random symmetric biases added in"""
        n = len(self.speakers)  # TODO why this line ???
        transitions = np.random.randint(5, size=(n, n)) + 1
        transitions += transitions.transpose()
        for i in range(0, math.floor(n / 2)):
            s1 = np.random.randint(n)
            s2 = np.random.randint(n)
            transitions[s1][s2] += 10
            transitions[s2][s1] += 8
        return(transitions)

    def after(self, speaker_id):
        """Pick next person to speak"""
        row = self._transitions[speaker_id]
        sucessor = searchsorted(cumsum(row), rand() * sum(row))
        return sucessor

    def speaker_sequence(self, speaker_id, n):
        """Random walk through transitions matrix to produce a sequence of speaker ids"""
        seq = []
        for i in range(n):
            seq.append(speaker_id)
            speaker_id = self.after(speaker_id)
        return seq

    def speech_sequence(self, n):
        speech_acts_seq = []
        next_speech_id = 0
        for i in range(n):
            next_speech_id = searchsorted(cumsum(self._acts_transitions), rand() * sum(self._acts_transitions))
            speech_acts_seq.append(self._speech_acts[next_speech_id])
        return speech_acts_seq

    def seq_to_names(self, sequence):
        return([self.speakers[id] for id in sequence])

    def make_speech_bits(self, seeds):
        n = len(seeds)
        speaker_id = self.speaker_sequence(0, n)
        speech_acts_seq = self.speech_sequence(n)
        bits = []
        ss = sentence.SentenceMaker(self.mc)
        for i in range(n):
            sent_toks = ss.generate_sentence_tokens([seeds[i]], self.target_len[speaker_id[i]])
            sent_toks = ss.polish_sentence(sent_toks)
            bits.append({'speaker_name': self.speakers[speaker_id[i]]["name"],
                         'speech_act': speech_acts_seq[speaker_id[i]],
                         'seq_id': speaker_id[i],
                         'speech': sent_toks,
                         'paragraph': True})
        return(bits)

    def simplify(self, seq_map):
        "Take a sequence of speech parts and make more natural by removing name reptition etc."
        for i in range(0, len(seq_map)):
            seq_map[i]['speaker_str'] = seq_map[i]['speaker_name']  # default
            # Same speaker contiues:
            if i > 0 and seq_map[i]['seq_id'] == seq_map[i - 1]['seq_id']:
                seq_map[i]['speaker_str'] = ""
                seq_map[i]['speech_act'] = ""
                seq_map[i]['paragraph'] = False
            else:
                if i > 1 and seq_map[i]['seq_id'] == seq_map[i - 2]['seq_id'] \
                   and seq_map[i]['seq_id'] != seq_map[i - 1]['seq_id']:
                    seq_map[i]['speaker_str'] = ""
                    seq_map[i]['speech_act'] = ""
                    seq_map[i]['paragraph'] = True
        return seq_map

    def report_seq(self, seq_map):
        """Convert sequence of speeches to a tokens."""
        sents = []
        for i in range(0, len(seq_map)):

            if seq_map[i]['paragraph']:
                # text += "\n    "
                quote_start = '"'
            else:
                quote_start = ""
            if i > len(seq_map) - 2 or seq_map[i + 1]['paragraph']:
                quote_end = '"'
            else:
                quote_end = " "
            if len(seq_map[i]['speech_act']) > 0:
                speech_act = seq_map[i]['speech_act'] + ","
            else:
                speech_act = seq_map[i]['speech_act']
            tokens = [utils.START_TOKEN]
            tokens.append(seq_map[i]['speaker_str'])
            tokens.append(speech_act)
            tokens.append(quote_start)
            tokens.extend(seq_map[i]['speech'][1:-1])
            tokens.append(quote_end)
            tokens.append(utils.END_TOKEN)
            sents.append(tokens)
        return sents

    def make_dialogue(self, seeds):
        """Returns a list of sentences, each being a list of tokens."""
        acts = self.make_speech_bits(seeds)
        seq_map = self.simplify(acts)
        sents = self.report_seq(seq_map)
        return(sents)


def dev():
    import knowledge.names as names

    mcW = mc.MarkovChain()
    nm = names.NameMaker()
    speakers = [nm.random_person() for i in range(1, 4)]
    dm = dialogue_maker([n['name'] for n in speakers], [n['pronoun'] for n in speakers], mcW)
    dlg = dm.make_dialogue(["dog", "run", "spot"])
    print(dlg)
