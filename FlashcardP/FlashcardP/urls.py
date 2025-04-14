
from django.contrib import admin
from django.urls import path, include
from App.views import SignUpView, LoginView, flashcards_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('flashcards/', include('App.urls')),
    path('flashcards/', flashcards_view),
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
]

