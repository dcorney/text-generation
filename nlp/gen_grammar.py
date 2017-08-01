from json import load
from random import uniform, choice
from sys import argv
import knowledge.wordnet as thesaurus
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

class Grammar:
    def __init__(self, file):
        self._grammar = load(file)

    @classmethod
    def from_file(self, path):
        with open(path) as f:
            return Grammar(f)

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

def dev():
    gr = Grammar.from_file("resources/grammar_obj.json")
    seq= gr.generate()
    print(seq)
        #print(f)
    terms = [ac_to_text(f) for f in seq]
    print(" then ".join(terms))

