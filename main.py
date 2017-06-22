import markovchain.markovchain as mchain
import logging

FORMAT='%(asctime)s %(name)12ss %(funcName)12s() %(levelname)7s: %(message)s'
logging.basicConfig(filename='logs/textgen.log', level=logging.DEBUG, format=FORMAT,datefmt='%m/%d/%Y %H:%M:%S')

mc = mchain.MarkovChain()
#mc.add_text("this is another sentence")

#print(mc._store.get_weights("is:back"))
print(mc.get_probs(["this","is"]))
print(mc.predict(["this","is"], direction='forward'))