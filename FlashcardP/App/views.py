from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from App.models import User, Card
from .serializers import UserSerializer, CardSerializer, CategorySerializer, SignUpSerializer, LoginSerializer, UserLoginSerializer


# Vista para mostrar todas las flashcards
def flashcards_view(request):
    # Obtiene todas las flashcards de la base de datos
    flashcards = Card.objects.all()
    
    # Pasa las flashcards a la plantilla para que se muestren
    return render(request, 'flashcards.html', {'flashcards': flashcards})


class SignUpView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



