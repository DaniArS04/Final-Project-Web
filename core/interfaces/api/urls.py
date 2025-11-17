from django.urls import path
from .views.card_view import CardView
from .views.user_view import UserView
from .views.category_view import CategoryView

urlpatterns = [
    path('cards/', CardView.as_view()),
        path("users/", UserView.as_view()),
    path("categories/", CategoryView.as_view()),
]
