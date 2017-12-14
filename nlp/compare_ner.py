import time

from nltk.tag import StanfordNERTagger
from spacy.en import English
import nlp.tokenizer_stanford as tokenizer_stanford
import nlp.compare_tokenizers as compare_tokenizers

# Use Stanford+ to find sentences, then compare spaCy to StanfordNER on each sentence

nlp = English()


def ner(ner_types):
    #text = "This is a short piece of text. It has a few sentences. Let's see how the splitters work! It was written by Dr. Corney who wrote this. He went to St. Albans School, years back..."
    text = compare_tokenizers.load_text()
    sents = tokenizer_stanford.find_sentences(text)
    for s in sents[1:1500]:
        if 'stanford' in ner_types:
            tokens_entities = tokenizer_stanford.tokenize_sentence(s)
            #st_tokens = tokens_entities['tokens']
            st_entities = tokens_entities['entities']
            st_all = st_entities.get('PERSON', []) + st_entities.get('ORGANIZATION', []) + st_entities.get('LOCATION', [])
        if 'spacy' in ner_types:    
            doc = nlp(" ".join(s.split()))
            sp_entities = doc.ents
            #print(" ".join(sp_entities))
            sp_all=[]
            for e in sp_entities:
                if e.label_ in ["PERSON","ORG","GPE"]:
                    sp_all.append(e.text)

        if 'spacy' in ner_types and 'stanford' in ner_types:    
            if set(sp_all) != set(st_all):
                print("===========================")
                print(s)        
                print("Stanford found {} entities.".format(len(st_all)))
                print(" ".join(st_all))
                print("spaCy    found {} entities.".format(len(sp_entities)))
                print(" ".join(sp_all))

def dev():
    start_time=time.process_time()
    ner(['stanford','spacy'])
    elapsed_time = time.process_time() - start_time
    print(elapsed_time)

    # start_time=time.process_time()
    # ner(['stanford'])
    # elapsed_time = time.process_time() - start_time
    # print(elapsed_time)

    # start_time=time.process_time()
    # ner(['spacy'])
    # elapsed_time = time.process_time() - start_time
    # print(elapsed_time)



if __name__ == '__main__':
    dev()