
from django.contrib import admin
from django.urls import path, include
from App.views import SignUpView, LoginView, flashcards_view, login_status, signup_status

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('App.urls')),
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('flashcards/', flashcards_view),
    path('login-status/', login_status),
    path('signup_status/', signup_status),
]

