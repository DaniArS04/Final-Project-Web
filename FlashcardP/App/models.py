from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, primary_key=True)
    name = models.CharField(max_length=150)
    last_name= models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password= models.CharField(max_length=128)
    # Relación ManyToMany para las tarjetas favoritas de cada usuario
    favorites_cards= models.ManyToManyField('Card', blank=True, related_name='favorites_for')

    def __str__(self):
        return self.username

class Category(models.Model):
    # el campo "id" se crea solo como primary key
    category_name = models.CharField(max_length=100)

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # si se elimina una categoria se eliminan las tarjetas asociadas a ella
    difficulty = models.CharField(max_length=300, choices=DIFFICULTIES)

    def __str__(self):
        return self.question
