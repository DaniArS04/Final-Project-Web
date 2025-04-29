
from rest_framework import routers
from .api import UserViewSet, CardViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register('api/users', UserViewSet, 'FP_users')
router.register('api/cards', CardViewSet, 'FP_cards')
router.register('api/categories', CategoryViewSet, 'FP_categories')

urlpatterns = router.urls

