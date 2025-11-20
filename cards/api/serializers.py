from rest_framework import serializers
from cards.infrastructure.models import Card, Category

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
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)

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
