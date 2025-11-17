from rest_framework.views import APIView
from rest_framework.response import Response
from core.domain.models.category import Category
from core.application.dto.category_dto import CategoryDTO
from core.domain.services.category_service import CategoryService
from core.infrastructure.repositories.django_category_repository import DjangoCategoryRepository

class CategoryView(APIView):

    def get(self, request):
        service = CategoryService(DjangoCategoryRepository())
        categories = service.list_categories()
        dto = CategoryDTO(categories, many=True)
        return Response(dto.data)

    def post(self, request):
        service = CategoryService(DjangoCategoryRepository())
        dto = CategoryDTO(data=request.data)
        dto.is_valid(raise_exception=True)

        category = Category(
            id=None,
            name=dto.validated_data["name"],
            description=dto.validated_data.get("description")
        )

        new_category = service.create_category(category)
        return Response(CategoryDTO(new_category).data)