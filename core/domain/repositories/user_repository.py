from abc import ABC, abstractmethod

class IUserRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def save(self, user):
        pass
