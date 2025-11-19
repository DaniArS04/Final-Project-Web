from django.contrib import admin
from .models import Card, Category, Favorite, UserCardProgress

admin.site.register(Card)
admin.site.register(Category)
admin.site.register(Favorite)
admin.site.register(UserCardProgress)
