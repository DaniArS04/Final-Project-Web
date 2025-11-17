class CategoryService:
    def __init__(self, repository):
        self.repository = repository

    def list_categories(self):
        return self.repository.get_all()

    def create_category(self, category):
        return self.repository.save(category)
