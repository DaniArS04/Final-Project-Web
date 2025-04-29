
import re
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate 
from django.contrib.auth import get_user_model
from App.models import User, Card, Category

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    
# Si no cumplen los requisitos, se lanza un error con un mensaje visible desde el frontend.
    def validate_password(self, value):
        # Mmnimo 8 caracteres
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters.") 
        
        # Al menos una letra
        if not re.search(r'[A-Za-z]', value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        
        # Al menos un numero
        if not re.search(r'[0-9]', value):
            raise 
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError("The user does not exist.")

        if user.email != data['email']:
            raise serializers.ValidationError("Email does not match.")

        # Se concatena el nombre y apellido almacenados xq a Melissa se le ocurrio ponerlo junto  
        full_name_registered = f"{user.name} {user.last_name}"
        if full_name_registered.strip() != data['full_name'].strip():
            raise serializers.ValidationError("Full name does not match.")

        if not check_password(data['password'], user.password):
            raise serializers.ValidationError("Password is wrong.")

        data['user'] = user
        return data

User = get_user_model()

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}) 

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        # Para mayor seguridad
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        data["user"] = user
        return data
