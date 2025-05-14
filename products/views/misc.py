from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from products.models import Category, Review
from products.permissions import IsOwnerOrReadOnly, IsStaffOrReadOnly
from products.serializers import CategorySerializers, ReviewSerializers, OrderSerializers
from products.models import Order


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    permission_classes = [IsStaffOrReadOnly]  # default = AllowAny


class CustomPagination(PageNumberPagination):
    page_size = 4


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Order.objects.all()
    serializer_class = OrderSerializers


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
