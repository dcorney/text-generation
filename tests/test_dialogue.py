from context import dialogue as dialogue
from context import core as core
import numpy as np


def test_transitions():
    mc = core.markovchain.MarkovChain()
    dm = dialogue.dialogue_maker([], [], mc, [])
    t = dm.make_transition_probs()
    assert isinstance(t, np.ndarray)
    assert len(t) == 0  # no transitions as no speakers!

    dm = dialogue.dialogue_maker(["sp1", "sp2"], ["she", "he"], mc, [])
    t = dm.make_transition_probs()
    assert isinstance(t, np.ndarray)
    assert len(t) == 2
    assert len(t[0]) == 2  # 2x2 array as two speakers

    assert len(dm.speech_sequence(0)) == 0
    assert len(dm.speech_sequence(5)) == 5


def test_make_dialogue():
    mc = core.markovchain.MarkovChain()
    phrase = "dog cat cat dog dog dog"
    seeds = phrase.split(" ")
    dm = dialogue.dialogue_maker(["Alice", "Bob", "Carol", "Dan"], ["she", "he", "she", "he"], mc, seeds)
    dlg = dm.make_dialogue()
    print(dlg)
    assert isinstance(dlg, str)

    
