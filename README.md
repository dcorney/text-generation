# text-generation

A library to generate text, and ideally a full-length novel. Inspired by NaNoGenMo, though this is taking more than one month...

It's also a place for me to improve my Python and to try out new NLP-related libraries.

Basic structure:

* core - modules for generating text from a Markov Chain and forming sentences, paragraphs, blocks of dialogue etc.
* database - stores n-gram frequencies for Markov Chains in a Redis store. Also local file stores, AWS S3 access etc.
* knowledge - access to various external knowledge bases, such as Wikipedia, WordNet, people's names etc.
* nlp - tokenizers, part-of-speech taggers etc.
* tests - tests (!)

Entry point is main.py which sets up logging and then calls whichever part of the system I'm working on.

Most modules have a "dev()" function for locally-testing the module. These are liable to change / be removed, so shouldn't be relied on.

Comments and suggestions always welcome!