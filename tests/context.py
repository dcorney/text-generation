import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""Allow test modules to import functions from anywhere in the project"""

import database.redis_store
import core.markovchain
import core.dialogue as dialogue
import core.sentence as sentence
import knowledge.wikipedia as wikipedia
import knowledge.wordnet as wordnet
import knowledge.word_vectors as word_vectors
