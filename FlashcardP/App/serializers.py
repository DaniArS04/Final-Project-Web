
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate 
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from App.models import User, Card, Category

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class CardSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Card
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# Serializador para el registro
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ['name', 'last_name', 'username', 'email', 'password']
        extra_kwargs = {
            'name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("The user already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("The email is already registered.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# Serializador de inicio de seccion
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
