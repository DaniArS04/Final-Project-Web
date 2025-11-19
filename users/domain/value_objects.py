from dataclasses import dataclass

@dataclass(frozen=True)
class UserIdVO:
    value: int

@dataclass(frozen=True)
class EmailVO:
    value: str

    def __post_init__(self):
        if "@" not in self.value:
            raise ValueError("Email inválido")
