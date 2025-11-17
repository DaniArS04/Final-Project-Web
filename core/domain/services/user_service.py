class UserService:
    def __init__(self, repository):
        self.repository = repository

    def list_users(self):
        return self.repository.get_all()

    def create_user(self, user):
        return self.repository.save(user)
