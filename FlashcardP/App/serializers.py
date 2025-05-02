
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate 
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
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
User = get_user_model()
class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, validators=[validate_password])

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("The user already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("The email is already registered.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user

# Serializador de inicio de seccion
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

# Serializador para la actualizacion de cards
class CardUpdateSerializer(serializers.Serializer):
    card_id = serializers.IntegerField(read_only=True)  
    question = serializers.CharField(required=False, allow_blank=True)
    answer = serializers.CharField(required=False, allow_blank=True)
    difficulty = serializers.ChoiceField(choices=[
        ('easy', 'Easy'),
        ('intermediate', 'Intermediate'),
        ('hard', 'Hard'),
    ], required=False)
    category = serializers.CharField(required=False, allow_blank=True)

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question', instance.question)
        instance.answer = validated_data.get('answer', instance.answer)
        instance.difficulty = validated_data.get('difficulty', instance.difficulty)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance
    
# Serializador para eliminar cards
class CardDeleteSerializer(serializers.Serializer):
    card_id = serializers.IntegerField()

    def validate_card_id(self, value):
        # Validar que la tarjeta existe y pertenece al usuario
        request = self.context.get('request')
        user = request.user if request else None

        if not Card.objects.filter(id=value, owner=user).exists():
            raise serializers.ValidationError("Card not found or you do not have permission to delete it.")
        return value

