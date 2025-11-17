from core.domain.repositories.user_repository import IUserRepository
from core.infrastructure.orm_models import UserORM
from core.domain.models.user import User

class DjangoUserRepository(IUserRepository):

    def get_all(self):
        orm_users = UserORM.objects.all()
        return [
            User(u.id, u.username, u.email)
            for u in orm_users
        ]

    def save(self, user):
        orm = UserORM.objects.create(
            username=user.username,
            email=user.email
        )
        return User(orm.id, orm.username, orm.email)
