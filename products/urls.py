from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.views import ProductViewSet, ReviewViewSet, CategoryViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
