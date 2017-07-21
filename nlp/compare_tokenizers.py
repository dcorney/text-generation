# Compare NLTK and spaCy for sentence tokenization accuracy
from spacy.en import English
import itertools
from nltk import sent_tokenize

nlp = English()


def spacy_sentences(text):
    doc = nlp(" ".join(text.split()))
    sents = []
    for sentence in doc.sents:
        sents.append(sentence.text)
    return sents


def nltk_sentences(text):
    ss = sent_tokenize(text)
    for idx in range(1, len(ss)):
        if ss[idx-1][-1]=='"' and ss[idx][0].islower():
            ss[idx-1]=ss[idx-1] + " " + ss[idx]
            ss[idx]=" "
    return ss


def display_sentences(sents, title):
    print("\n=================\n{} found {:2d} sentences:\n".format(title, len(sents)))
    for idx, s in enumerate(sents):
        if idx > 0 and idx < 50:
            print("{:2d} {}".format(idx, s))


def display_comparison(sentsA, sentsB, titleA, titleB):
    w = 50
    print("\n=================\n{} found {:2d} sentences {:>{w}s} found {:2d} sentences\n".format(titleA, len(sentsA), titleB, len(sentsB), w=2 * w))
    for idx in range(1,50):
        print("{:2d} {:{w}s}...{:{w}s}  |  {:{w}s}...{:{w}s}".format(idx, sentsA[idx][:w], sentsA[idx][(w+10):][-w:], sentsB[idx][:w], sentsB[idx][(w+10):][-w:],w=w))
        #print("{:2d} {:{w}s}...{:ws}  |  {:ws}...{:ws}".format(idx, sentsA[idx][:w], sentsA[idx][w:][-w:], sentsB[idx][:w], sentsB[idx][w:][-w:],w=w))

def load_text():
    filename = "/Users/dcorney/temp/112.txt"
    with open(filename, 'r') as myfile:
        text = myfile.read().replace('\n', ' ')
    print("Loaded {} - {} characters".format(filename, len(text)))
    return text[5000:50000]


def dev():
    #text = "This is a short piece of text. It has a few sentences. Let's see how the splitters work! It was written by Dr. Corney who wrote this. He went to St. Albans School, years back..."
    text = load_text()
    nltk_sents = nltk_sentences(text)
    spacy_sents = spacy_sentences(text)
    display_sentences(nltk_sents, "NLTK")
    display_sentences(spacy_sents, "spaCy")
    #display_comparison(nltk_sents, spacy_sents, "NLTK", "spaCy")


if __name__ == '__main__':
    dev()
