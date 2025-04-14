from django.contrib import admin
from .models import User, Card, Category

class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'name', 'last_name', 'email', 'password']
    list_display = ['username']
admin.site.register(User, UserAdmin)

class CardAdmin(admin.ModelAdmin):
    fields = ['card_id', 'question', 'answer', 'category', 'get_difficulty_display']
    list_display = ['card_id','get_difficulty_display']
admin.site.register(Card, CardAdmin)

class CategoryAdmin(admin.ModelAdmin):
    fields = ['category_name']
admin.site.register(Category, CategoryAdmin)