from json import load
from random import uniform, choice
from sys import argv
import knowledge.thesaurus as thesaurus
import knowledge.word_vectors as w2v

#From https://gist.github.com/FLamparski/717bb8bd708dae6d4d48

def all(xs, f):
    return len(xs) == len([x for x in xs if f(x)])

def grammar_choice(rules):
    if (len(rules) == 1):
        return rules[0]

    if not all(rules, lambda r: 'weight' in r):
        return choice(rules)

    total = sum(r['weight'] for r in rules)
    v = uniform(0, total)
    upto = 0
    for r in rules:
        if upto + r['weight'] >= v:
            return r
        else:
            upto += r['weight']

# class Grammar:
#     def __init__(self, file):
#         self._grammar = load(file)

#     @classmethod
#     def from_file(self, path):
#         with open(path) as f:
#             return Grammar(f)

#     def generate(self):
#         def on_token(t):
#             return t if isinstance(t, str) else walk(t['var'])
#         def walk(symbol):
#             rule = grammar_choice(self._grammar[symbol])
#             return ' '.join(on_token(t) for t in rule['production'])
#         return walk('S')

class Grammar_obj:
    def __init__(self, file):
        self._grammar = load(file)

    @classmethod
    def from_file(self, path):
        with open(path) as f:
            return Grammar_obj(f)

    def generate(self):
        seq=[]
        def on_token(t):
            if 'var' in t:
                walk(t['var'])
            else:
                seq.append(t['ac'])
        def walk(symbol):
            rule = grammar_choice(self._grammar[symbol])
            for t in rule['prod']:
                on_token(t)
        walk('S')
        return(seq)

world={"protag1":"Alice", "protag2":"Bert", "protag3":"Charlie",
    "antag1":"Walter",
    "item1":"toy",
    "loc1":"London","loc2":"Paris","loc3":"Berlin","loc4":"London"}

#TODO: generate (or take as input) a markovchain sequence of tokens;
#then analyse those for POS tags
#then replace the corresponding nouns/verbs with the subject/verb/object of the action category!
#ALSO: actions should 'write' to the world - e.g. moving an object or allowing links between remote actions.
#So if one action writes 'complication=villainy' then later on, the resolution should chose 'resolve-villainy' and not 'resolve-lack'
#Or do proper transformations that keep track explicitly?
def ac_to_text(ac):
    """Convert an action-category object to a sequence of tokens"""
    actor = world.get(ac.get('subj'))
    action = ac.get("act")
    #action = w2v.synonym(action) if uniform(0,1)<0.5 else thesaurus.synonym(action)
    action = thesaurus.synonym(action)
    obj = ac.get("obj","")
    if obj != "":
        obj=world.get(obj,obj)
    obj = thesaurus.synonym(obj)
    phrase = " ".join([actor, action, obj]).strip()
    return(phrase)

def dev():
    seq=Grammar_obj.from_file("resources/grammar_obj.json").generate()
    print(seq)
        #print(f)
    terms = [ac_to_text(f) for f in seq]
    print(" then ".join(terms))

