from core.domain.repositories.category_repository import ICategoryRepository
from core.infrastructure.orm_models import CategoryORM
from core.domain.models.category import Category

class DjangoCategoryRepository(ICategoryRepository):

    def get_all(self):
        orm_categories = CategoryORM.objects.all()
        return [
            Category(c.id, c.name, c.description)
            for c in orm_categories
        ]

    def save(self, category):
        orm = CategoryORM.objects.create(
            name=category.name,
            description=category.description
        )
        return Category(orm.id, orm.name, orm.description)
