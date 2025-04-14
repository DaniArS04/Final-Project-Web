from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.category_name

# se cambio de aqui el atributo favoritos xq ya se hace funcion en el manytomany
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
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='cards')

    def __str__(self):
        return self.question

class User(models.Model):
    username = models.CharField(max_length=150, primary_key=True)
    name = models.CharField(max_length=150)
    last_name= models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password= models.CharField(max_length=128)

    def __str__(self):
        return self.username


