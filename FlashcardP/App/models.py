from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class User(AbstractUser):
    first_name = models.CharField(max_length=150, verbose_name='Name', blank=True, null=True)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    category_name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.category_name


class Card(models.Model):
    DIFFICULTIES = [
        ('easy', 'Easy'),
        ('intermediate', 'Intermediate'),
        ('hard', 'Hard'),
    ]
    card_id = models.AutoField(primary_key=True)
    question = models.TextField()
    answer = models.TextField()
    difficulty = models.CharField(max_length=300, choices=DIFFICULTIES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # si se elimina una categoria se eliminan las tarjetas asociadas a ella
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='cards', default=1)


    def __str__(self):
        return self.question


User = get_user_model()
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    card = models.ForeignKey('Card', on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'card')

