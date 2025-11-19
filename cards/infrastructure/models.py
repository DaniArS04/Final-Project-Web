from django.db import models
from django.conf import settings

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Card(models.Model):
    DIFFICULTIES = (
        ("easy", "Easy"),
        ("intermediate", "Intermediate"),
        ("hard", "Hard"),
    )

    question = models.TextField()
    answer = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTIES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    created_by = models.DateTimeField(auto_now_add=True)

class UserCardProgress(models.Model):
    STATES = (
        ('dominates', 'Dominates'), 
        ('does_not_dominate', 'Does_not_Dominate')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    state = models.CharField(max_length=20, choices=STATES)
