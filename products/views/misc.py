from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import models
from django_filters import rest_framework as django_filters
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from products.filters import ProductFilter
from products.models import Category, Review, Product
from products.serializers import CategorySerializers, ReviewSerializers, ProductSerializers


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class CustomPagination(PageNumberPagination):
    page_size = 4


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
