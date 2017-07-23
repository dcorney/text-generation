import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import database.redis_store
import core.markovchain
import core.dialogue as dialogue
import core.sentence as sentence
import knowledge.wikipedia as wiki
