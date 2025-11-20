from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken import RefreshToken
from django.forms import ValidationError
from cards.infrastructure.models import Card
from users.api.serializers import SignupSerializer, UserLoginSerializer, CardSerializer

# Maneja la obtencion de todas las cartas de el user auntenticado a traves de una solicitud GET: http://127.0.0.1:8000/api/auth/flashcards/
class FlashcardListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            flashcards = Card.objects.filter(owner = request.user)
            
            if not flashcards.exists():
                return Response(
                    {'error': 'No flashcards available'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = CardSerializer(flashcards, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Maneja el registro de usuarios 
class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                user = serializer.save()
                
                # Generar tokens JWT
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Successfully registered user',
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, status=status.HTTP_201_CREATED)
            
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # Manejar errores de validación del serializer
        return Response({
            'error': 'Validation error',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# Maneja el inicio de seccion del usuario 
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
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

# Maneja una solicitud POST donde se separa el nombre del apellido para agg en la BD
def process_full_name(full_name):
    name_parts = full_name.split(" ", 1)  # Separa solo en el primer espacio
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ""  # Si no hay apellido, se deja vacio
    return first_name, last_name

class ValidateCompleteNameView(APIView):
    def post(self, request, *args, **kwargs):
        complete_name = request.data.get("complete_name", "").strip()

        if not complete_name:
            return Response({"error": "Complete name is required"}, status=status.HTTP_400_BAD_REQUEST)

        first_name, last_name = process_full_name(complete_name)

        return Response({
            "message": "Successful validation",
            "name": first_name,
            "last_name": last_name
        }, status=status.HTTP_200_OK)

# Maneja la obtencion de el username de user autenticado
class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({'username': request.user.username})

# Maneja la eliminacion de un usuario 
class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request):
        try:
            user = request.user
            user.delete()
            return Response({'message': 'User successfully removed..'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        