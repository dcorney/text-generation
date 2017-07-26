from nltk.corpus import names
import random


class NameMaker(object):
    def __init__(self):
        self.male_names = names.words('male.txt')
        self.female_names = names.words('female.txt')

    def random_male(self):
        return(random.choice(self.male_names))

    def random_female(self):
        return(random.choice(self.female_names))

    def random_person(self):
        if random.random() < 0.5:
            return {"gender": "female", "pronoun":"she", "name": self.random_female()}
        else:
            return {"gender": "male", "pronoun":"he", "name": self.random_male()}
