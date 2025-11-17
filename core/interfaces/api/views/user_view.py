from rest_framework.views import APIView
from rest_framework.response import Response
from core.domain.models.user import User
from core.application.dto.user_dto import UserDTO
from core.domain.services.user_service import UserService
from core.infrastructure.repositories.django_user_repository import DjangoUserRepository

class UserView(APIView):

    def get(self, request):
        service = UserService(DjangoUserRepository())
        users = service.list_users()
        dto = UserDTO(users, many=True)
        return Response(dto.data)

    def post(self, request):
        service = UserService(DjangoUserRepository())
        dto = UserDTO(data=request.data)
        dto.is_valid(raise_exception=True)

        user = User(
            id=None,
            username=dto.validated_data["username"],
            email=dto.validated_data["email"]
        )

        new_user = service.create_user(user)
        return Response(UserDTO(new_user).data)
