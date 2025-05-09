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


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    permission_classes = [IsAuthenticated]     # default = AllowAny

    pagination_class = CustomPagination  # api/products/?page=2

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ['name', 'description']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, description="Category ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('min_price', openapi.IN_QUERY, description="Minimal price", type=openapi.TYPE_NUMBER),
            openapi.Parameter('max_price', openapi.IN_QUERY, description="Maximal price", type=openapi.TYPE_NUMBER),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search in name or description",
                              type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category', None)
        if category:
            self.queryset = self.queryset.filter(category=category)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_products = Product.objects.filter(category=instance.category).exclude(id=instance.id)[:5]
        related_serializer = ProductSerializers(related_products, many=True)
        return Response({
            "product": serializer.data,
            "related_products": related_serializer.data
        })

    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        top_products = Product.objects.annotate(avg_rating=models.Avg('reviews__rating')).order_by('-avg_rating')[:2]
        serializer = ProductSerializers(top_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def average_rating(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all()

        if reviews.count() == 0:
            return Response({'Average rating: No reviews yet'})

        avg_rating = sum(reviews.rating for _ in reviews) / reviews.count()
        return Response({"Average rating:", avg_rating})
