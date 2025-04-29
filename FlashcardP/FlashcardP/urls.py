
from django.contrib import admin
from django.urls import path, include
from App.views import FlashcardListView, LoginView, SignupView, ValidateCompleteNameView, DeleteUserView, CardCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('App.urls')),
    path('api/users/login/', LoginView.as_view(), name='login'), # url para la solicitud de inicio de seccion de usuario
    path('api/users/signup/', SignupView.as_view(), name='signup'), # url para la solicitud de registro de usuario
    path('api/users/validate-name/', ValidateCompleteNameView.as_view(), name='validate_complete_name'), # url para la union del nombre y apellido de el registro
    path('api/users/delete-user/<str:username>/', DeleteUserView.as_view(), name='delete_user'), # url para eliminar un usuario
    path('api/cards/flashcards/', FlashcardListView.as_view(), name='flashcards-list'), # url para obtener todas las cartas 
    path('api/cards/create/', CardCreateView.as_view(), name='card-create'), 
]

