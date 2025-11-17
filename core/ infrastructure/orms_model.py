
from django.db import models

class UserORM(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='Name', blank=True, null=True)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.user

class CategoryORM(models.Model):
    category_name = models.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey(UserORM, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.category_name

class CardORM(models.Model):
    DIFFICULTIES = [
        ('easy', 'Easy'),
        ('intermediate', 'Intermediate'),
        ('hard', 'Hard'),
    ]
    card_id = models.AutoField(primary_key=True)
    question = models.TextField()
    answer = models.TextField()
    difficulty = models.CharField(max_length=300, choices=DIFFICULTIES)
    category_name = models.ForeignKey(CategoryORM, on_delete=models.CASCADE) # si se elimina una categoria se eliminan las tarjetas asociadas a ella
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='cards', default=1)

    def __str__(self):
        return self.question

class FavoriteORM(models.Model):
    user = models.ForeignKey(UserORM, on_delete=models.CASCADE, related_name='favorites')
    card = models.ForeignKey('Card', on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'card_id')

class UserCardProgressORM(models.Model):
    user = models.ForeignKey(UserORM, on_delete=models.CASCADE, default=1)
    card_id = models.IntegerField()
    state = models.CharField(max_length=20, choices=[('dominates', 'Dominates'), ('does_not_dominate', 'Does_not_Dominate')])

    class Meta:
        unique_together = ('user', 'card_id')

        