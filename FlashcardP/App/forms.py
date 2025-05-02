from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from .models import User  

class CustomUserCreationForm(AdminUserCreationForm): 
    class Meta(AdminUserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name")  
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
