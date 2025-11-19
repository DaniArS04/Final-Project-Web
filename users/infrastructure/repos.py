from django.contrib.auth.models import User
from users.domain.entities import UserEntity
from users.domain.value_objects import EmailVO, UserIdVO
from users.domain.repository import UserRepository

class DjangoUserRepository(UserRepository):

    def create_user(self, first_name, last_name, email, password):
        user = User.objects.create_user(
            username=email,   # usamos email como username
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        return UserEntity(
            id=UserIdVO(user.id),
            first_name=user.first_name,
            last_name=user.last_name,
            email=EmailVO(user.email)
        )

    def get_by_email(self, email):
        try:
            user = User.objects.get(email=email)
            return UserEntity(
                id=UserIdVO(user.id),
                first_name=user.first_name,
                last_name=user.last_name,
                email=EmailVO(user.email)
            )
        except User.DoesNotExist:
            return None
