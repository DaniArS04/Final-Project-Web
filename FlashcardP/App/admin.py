from django.contrib import admin
from .models import User, Card, Category
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']

admin.site.register(User, CustomUserAdmin)
class CardAdmin(admin.ModelAdmin):
    fields = ['question', 'answer', 'category', 'owner', 'difficulty']  
    list_display = ['card_id', 'question', 'answer', 'difficulty', 'get_difficulty_display']  
    readonly_fields = ['get_difficulty_display']  
admin.site.register(Card, CardAdmin)


class CategoryAdmin(admin.ModelAdmin):
    fields = ['category_name']  
    list_display = ['category_name']  
    search_fields = ['category_name']

admin.site.register(Category, CategoryAdmin)
