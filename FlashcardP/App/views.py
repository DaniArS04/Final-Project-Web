
from django.forms import ValidationError
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from App.models import User, Card
from .serializers import  CardSerializer, UserLoginSerializer, SignupSerializer

# Maneja la obtencion de todas las cartas a traves de una solicitud GET: http://127.0.0.1:8000/api/auth/flashcards/
class FlashcardListView(APIView):
    def get(self, request):
        try:
            flashcards = Card.objects.all()
            
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

# Maneja el registro de usuarios a traves de una solicitud POST: http://127.0.0.1:8000/api/auth/signup/
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

# Maneja el inicio de seccion del usuario a traves de una solicitud POST: http://127.0.0.1:8000/api/auth/login/
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
class CardCreateView(APIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]  # Solo usuarios autenticados

    # Asigna automaticamente el owner como el usuario actual
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)