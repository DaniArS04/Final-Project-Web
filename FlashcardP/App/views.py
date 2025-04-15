from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from App.models import User, Card
from .serializers import UserSerializer, CardSerializer, CategorySerializer, SignUpSerializer, LoginSerializer, UserLoginSerializer
import json

# Vista para mostrar todas las flashcards
def get_flashcards(request):
    if request.method == 'GET':
        # Obtiene todas las flashcards de la base de datos
        flashcards = Card.objects.all().values('card_id', 'question', 'answer', 'difficulty', 'category', 'owner' )
        if not flashcards:  # Verifica si el queryset esta vacio
            return JsonResponse({'error': 'No flashcards available'}, status=404)
        return JsonResponse(list(flashcards), safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

class SignUpView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomSignupView(APIView):
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

def signup(request):
    if request.method == 'POST':
        try:
            # Parsear los datos enviados en el cuerpo de la solicitud
            data = json.loads(request.body)
            username = data.get('username')
            name = data.get('name')
            last_name = data.get('last_name')
            email = data.get('email')
            password = data.get('password')

            # Validar que los datos requeridos estén presentes
            if not username or not name or not last_name or not email or not password:
                return JsonResponse({'error': 'All fields are mandatory'}, status=400)

            # Crear un nuevo usuario
            user = User.objects.create_user(username=username, name=name, last_name=last_name, email=email, password=password)
            user.save()

            return JsonResponse({'message': 'Successfully registered user'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

class ValidateCompleteNameView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': 'Successful validation'}, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Autenticaion mediante tokens para mayor seguridad
class CustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return Response({'mensaje': 'Successful login', 'tokens': response.data}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def login(request):
    if request.method == 'POST':
        try:
            # Parsear los datos enviados en el cuerpo de la solicitud
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            if not username or not password:
                return JsonResponse({'error': 'Username and password are mandatory'}, status=400)

            # Autenticar el usuario
            user = authenticate(username=username, password=password)
            if user is not None:
                # Si la autenticacion es exitosa, devuelve la información del usuario
                return JsonResponse({'message': 'Successful login', 'username': user.username}, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
