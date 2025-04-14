from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from App.models import User, Card
from .serializers import UserSerializer, CardSerializer, CategorySerializer, SignUpSerializer, LoginSerializer, UserLoginSerializer
# from forms import RegistroForm


# Vista para mostrar todas las flashcards
def flashcards_view(request):
    # Obtiene todas las flashcards de la base de datos
    flashcards = Card.objects.all()

class SignUpView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def signup_status(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()  # Crea el usuario
            login(request, user)  # Autentica y loguea al usuario
            return redirect('home')  # Redirige a página principal
    else:
        form = RegistroForm()
    
    # return render(request, 'registration/registro.html', {'form': form})


class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required  # Asegura que solo usuarios autenticados puedan acceder
def login_status(request):
    if request.method == 'GET':
        username = request.user.username
        name = request.user.username
        last_name = request.user.last_name
        email = request.user.email
        password = request.user.password
        
        # Devuelve los datos del usuario en formato JSON
        return JsonResponse({
            'status': 'success',
            'username': username,
            'name': 'name',
            'last_name': 'last_name',
            'email': email,
            'password': 'password'
        })
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


