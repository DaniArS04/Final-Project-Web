
from django.shortcuts import get_object_or_404
from django.forms import ValidationError
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, ListAPIView, CreateAPIView
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from App.models import User, Card, Category, Favorite
from .serializers import  UserSerializer, CardSerializer, UserLoginSerializer, CategorySerializer, SignupSerializer, CardUpdateSerializer, ChangeUserSerializer

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

#-------------------------Todas las vistas relacionadas con el user-----------------------------------------------#
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
    
# Maneja una solicitud POST donde se separa el nombre del apellido para agg en la BD: http://127.0.0.1:8000/api/auth/validate-name/ 
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
    
# Maneja la obtencion de el username de user autenticado
class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({'username': request.user.username})

# Maneja la eliminacion de un usuario a traves de una solicitud DELETE: http://127.0.0.1:8000/api/users/delete-user/
class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request):
        try:
            user = request.user
            user.delete()
            return Response({'message': 'User successfully removed..'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# Actualizacion de datos del user
class ChangeUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        serializer = ChangeUserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.username = serializer.validated_data['username']

            new_password = serializer.validated_data.get('new_password')
            if new_password:
                user.set_password(new_password)

            user.save()
            return Response({"detail": "User updated correctly."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#-------------------------Todas las vistas relacionadas con las Cards-----------------------------------------------#
# Maneja la creacion de cartas a traves de una solicitud POST http://127.0.0.1:8000/api/auth/create/

class CardCreateListView(ListCreateAPIView):
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Card.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {"detail": "No cards available for this user."},
                status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#-------------------------Todas las vistas relacionadas con las Categories dentro de las Cards-------------------------------------------#
# Maneja la solicitud de obtener todas las categorias existentes a traves de un POST http://127.0.0.1:8000/api/auth/
class CardCreateListView(ListCreateAPIView):
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Card.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {"detail": "No cards available for this user."},
                status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# Maneja la muestra de todas las categorias a traves de una solicitud GET http://127.0.0.1:8000/api/auth/ 
class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Filtra solo las categorias creadas por el usuario actual
            return Category.objects.filter(user=user)
        # Si el usuario no esta autenticado, retorna un queryset vacio
        return Category.objects.none()
    
# Maneja la creacion de una nueva categoria a traves de una solicitud POST http://127.0.0.1:8000/api/auth/
class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated] 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

# Maneja la solicitud de actualizacion de cards a traves de una solicitud UPDATE: http://127.0.0.1:8000/api/auth/<int:pk>/
class CardUpdateView(UpdateAPIView):
    serializer_class = CardUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return Card.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response({
            'message': 'Card updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

# Maneja la solicitud de eliminacion de cards a traves de una solicitud DELETE: http://127.0.0.1:8000/api/auth/<int:pk>/
class CardDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, card_id, *args, **kwargs): 
        card = get_object_or_404(Card, card_id=card_id, owner=request.user)
        card.delete()
        return Response({"detail": "Card deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

# Maneja la solicitud de obtener todas las categorias(una card por categoria)
class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Maneja la solicitud de listar todos los Elementos de una Categoría
class CardByCategoryListView(ListAPIView):
    serializer_class = CardSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Card.objects.filter(category_id=category_id)

# Maneja la solicitud de filtrar categoria y dificultad 
class CardCategoryListView(ListAPIView):
    serializer_class = CardSerializer

    def get_queryset(self):
        queryset = Card.objects.all()
        category_id = self.kwargs.get('category_id')  # Se obtiene de la URL
        difficulty = self.request.query_params.get('difficulty')  # Se obtiene de los parámetros GET

        if category_id:
            queryset = queryset.filter(category_id=category_id)  # Filtra por categoría
        if difficulty:
            queryset = queryset.filter(difficulty__iexact=difficulty)  # Filtra por dificultad (case-insensitive)
        return queryset

#--------------------------Todos las vistas relacionadas con Favoritos----------------------------------------#
# Maneja la solicitud de agregar/quitar favoritos a traves de una solicitud POST/DELETE: http://127.0.0.1:8000/api/auth/<int:pk>/
class FavoriteCardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, card_id):
        card = Card.objects.get(pk=card_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, card=card)
        if created:
            return Response({'detail': 'Card added to favorites.'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Card already in favorites.'}, status=status.HTTP_200_OK)

    def delete(self, request, card_id):
        try:
            favorite = Favorite.objects.get(user=request.user, card_id=card_id)
            favorite.delete()
            return Response({'detail': 'Card removed from favorites.'}, status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response({'detail': 'Card not in favorites.'}, status=status.HTTP_404_NOT_FOUND)
        
# Maneja la solicitud de obtener todas las cards marcadas como favoritas a traves de una solicitud GET: http://127.0.0.1:8000/api/cards/favorites/
class FavoriteListView(ListAPIView):
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Card.objects.filter(favorited_by__user=self.request.user)

