
from django.contrib import admin
from django.urls import path, include
from App.views import FlashcardListView, LoginView, SignupView, ValidateCompleteNameView, DeleteUserView
from App.views import  CardCreateListView, CategoryListView, CategoryCreateView, CardUpdateView, CardDeleteView, FavoriteCardView, FavoriteListView, CardByCategoryListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('App.urls')),
    path('api/auth/login/', LoginView.as_view(), name='login'), # url para la solicitud de inicio de seccion de usuario
    path('api/auth/signup/', SignupView.as_view(), name='signup'), # url para la solicitud de registro de usuario
    path('api/auth/validate-name/', ValidateCompleteNameView.as_view(), name='validate_complete_name'), # url para la union del nombre y apellido de el registro
    path('api/auth/delete-user/<str:username>/', DeleteUserView.as_view(), name='delete_user'), # url para la solicitud de eliminacion de usuario
    path('api/auth/flashcards/', FlashcardListView.as_view(), name='flashcards-list'), # url para la solicitud de obtener todas las cartas del user autenticado
    path('api/auth/create-card/', CardCreateListView.as_view(), name='card-create'), # url para la solicitud de crear una nueva carta
    path('api/auth/categories/', CategoryListView.as_view(), name='category-list'), # url para la solicitud de listar categorías existentes
    path('api/auth/<int:pk>/', CardUpdateView.as_view(), name='card-update'), # url para la solicitud de actualizacion de cards
    path('api/auth/<int:card_id>/delete/', CardDeleteView.as_view(), name='card-delete'), # url para la solicitud de eliminacion de cards
    path('api/auth/<int:card_id>/favorite/', FavoriteCardView.as_view(), name='card-favorite'), # url para la solicitud de agg/quitar favoritos
    path('api/auth/favorites/', FavoriteListView.as_view(), name='favorite-list'), # url para la solicitud de obtener las cards favoritas
    path('api/auth/add/', CategoryCreateView.as_view(), name='category-add'), # url para la solicitud de crear una nueva categoría
    path('api/auth/categories/', CategoryListView.as_view(), name='category-list'),
    path('api/auth/<int:category_id>/cards/', CardByCategoryListView.as_view(), name='cards-by-category'),
]

