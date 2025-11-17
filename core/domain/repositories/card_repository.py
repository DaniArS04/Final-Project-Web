
from abc import ABC, abstractmethod

class ICardRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def save(self, card):
        pass
