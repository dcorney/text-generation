import abc


class Synonymizer(abc.ABC):
    """Abstract class for thesaurses etc. that generate synonyms"""
    @abc.abstractmethod
    def synonym(self, word):
        pass

    @abc.abstractmethod
    def synonyms(self, word_list, n):
        """Returns list containing total of n synonyms based on the provided list"""
        pass

    @abc.abstractmethod
    def path(self, word, n):
        """Returns list containing total of n words, each related to the previous one"""
        pass
