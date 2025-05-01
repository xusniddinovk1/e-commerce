from django.urls import path, include
from rest_framework import routers
from .views import CategoryViewSet, ProductViewSet, ReviewViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls))
]
