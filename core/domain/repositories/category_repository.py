from abc import ABC, abstractmethod

class ICategoryRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def save(self, category):
        pass

