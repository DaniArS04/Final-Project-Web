
from django.contrib import admin
from django.urls import path, include
from App.views import SignUpView, LoginView, get_flashcards, login, signup, CustomLoginView, CustomSignupView, ValidateCompleteNameView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('App.urls')),
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('flashcards/', get_flashcards, name='get_flashcards'),
    path('login_status/', login, name='login'),
    path('signup_status/', signup, name='signup'),
    path('api/login/', CustomLoginView.as_view(), name='custom_login'),
    path('api/signup/', CustomSignupView.as_view(), name='custom_signup'),
    path('api/validate-complete-name/', ValidateCompleteNameView.as_view(), name='validate_complete_name'),

]

