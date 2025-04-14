
from django.contrib import admin
from django.urls import path, include
from App.views import SignUpView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('flashcards/', include('App.urls')),
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
]