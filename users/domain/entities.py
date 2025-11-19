from dataclasses import dataclass
from users.domain.value_objects import EmailVO, UserIdVO

@dataclass
class UserEntity:
    id: UserIdVO
    first_name: str
    last_name: str
    email: EmailVO
