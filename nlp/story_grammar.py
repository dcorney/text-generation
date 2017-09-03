import nlp.gen_grammar as grammar
import knowledge.wordnet as wn_thesaurus
import nlp.pos as pos
import pprint 

thesaurus = wn_thesaurus.WordNet()

world={"protag1":"Alice", "protag2":"Bert", "protag3":"Christine",
    "antag1":"Walter",
    "item1":"toy",
    "loc1":"London","loc2":"Paris","loc3":"Berlin","loc4":"London"}


def swap_tokens(sentence, new_verb, new_noun):
    verbs = pos.verbs(sentence)
    nouns = pos.nouns(sentence)
    # print(verbs)
    # print(nouns)
    if verbs:
        new_s = [token if token != verbs[0] else new_verb for token in sentence]
    else:
        new_s = sentence
    if nouns:
        new_s = [token if token != nouns[0] else new_noun for token in new_s]
    return new_s


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
    #action = thesaurus.synonym(action)
    obj = ac.get("obj","")
    if obj != "":
        obj=world.get(obj,obj)
    #obj = thesaurus.synonym(obj)
    phrase = " ".join([actor, action, obj]).strip()
    return({"actor":actor, "action":action, "object":obj, "phrase":phrase})


def make_story(sentence_generator):
    gr = grammar.Grammar.from_file("resources/grammar_obj.json")
    seq= gr.generate()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(seq)
    terms = [ac_to_text(f) for f in seq]
    seeds = thesaurus.path("table", n=len(terms))
    phrases = [t['phrase'] for t in terms]

    print(" then ".join(phrases))

    for i,t in enumerate(terms):
        #print("{}: {}".format(i,t))
        s = sentence_generator.generate_sentence_tokens([seeds[i]],target_length=10)
        new_s = swap_tokens(s, t["action"], t["actor"])
        cs = sentence_generator.polish_sentence(new_s)
        print(sentence_generator.to_string(cs))

