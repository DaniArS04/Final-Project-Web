from abc import ABC, abstractmethod
from users.domain.entities import UserEntity

class UserRepository(ABC):

    @abstractmethod
    def create_user(self, first_name: str, last_name: str, email: str, password: str) -> UserEntity:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> UserEntity | None:
        pass
