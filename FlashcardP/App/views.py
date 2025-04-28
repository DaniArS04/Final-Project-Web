
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView, View
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from App.models import User, Card
from .serializers import UserSerializer, CardSerializer, CategorySerializer, SignUpSerializer, LoginSerializer, UserLoginSerializer

# Maneja la obtencion de todas las cartas a traves de una solicitud GET: http://127.0.0.1:8000/api/cards/flashcards/
class FlashcardListView(View):
    def get(self, request):
        try:
            flashcards = Card.objects.all().values(
                'card_id',
                'question',
                'answer',
                'difficulty',
                'category',
                'owner'
            )
            
            if not flashcards:
                return JsonResponse(
                    {'error': 'No flashcards available'}, 
                    status=404
                )
                
            return JsonResponse(list(flashcards), safe=False)
            
        except Exception as e:
            return JsonResponse(
                {'error': str(e)}, 
                status=500
            )

# Maneja el registro de usuarios a traves de una solicitud POST: http://127.0.0.1:8000/api/users/signup/
class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Obtener los datos del cuerpo de la solicitud
            username = request.data.get('username')
            name = request.data.get('name')
            last_name = request.data.get('last_name')
            email = request.data.get('email')
            password = request.data.get('password')

            # Validar que todos los campos esten presentes
            if not username or not name or not last_name or not email or not password:
                return Response({'error': 'All fields are mandatory'}, status=status.HTTP_400_BAD_REQUEST)

            # Verificar si el usuario ya existe
            if User.objects.filter(username=username).exists():
                return Response({'error': 'The user already exists'}, status=status.HTTP_400_BAD_REQUEST)

            # Crear un nuevo usuario
            user = User.objects.create_user(username=username, name=name, last_name=last_name, email=email, password=password)
            user.save()

            # Generar tokens JWT
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Successfully registered user',
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Maneja el inicio de seccion del usuario a traves de una solicitud GET: http://127.0.0.1:8000/api/users/login/
class LoginView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            
            # Generar tokens JWT
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


def process_full_name(full_name):
    name_parts = full_name.split(" ", 1)  # Separa solo en el primer espacio
    name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ""  # Si no hay apellido, se deja vacio
    return name, last_name

# Maneja una solicitud POST donde se separa el nombre del apellido para agg en la BD: http://127.0.0.1:8000/api/users/validate-name/ 
class ValidateCompleteNameView(APIView):
    def post(self, request, *args, **kwargs):
        complete_name = request.data.get("complete_name", "").strip()

        if not complete_name:
            return Response({"error": "Complete name is required"}, status=status.HTTP_400_BAD_REQUEST)

        name, last_name = process_full_name(complete_name)

        return Response({
            "message": "Successful validation",
            "name": name,
            "last_name": last_name
        }, status=status.HTTP_200_OK)

# Maneja la eliminacion de un usuario a traves de una solicitud DELETE: http://127.0.0.1:8000/api/users/delete-user/
class DeleteUserView(APIView):
    def delete(self, request, username):
        try:
            user = User.objects.get(pk=username)
            user.delete()
            return Response({'message': 'User successfully removed..'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        

# Maneja la creacion de cartas a traves de una solicitud POST http://127.0.0.1:8000/api/cards/create/
class CardCreateView(generics.CreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]  # Solo usuarios autenticados

    # Asigna automaticamente el owner como el usuario actual
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)