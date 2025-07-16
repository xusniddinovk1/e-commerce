from django.db import models
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as django_filters
from rest_framework.decorators import action
from rest_framework.response import Response
from products.filters import ProductFilter
from products.models import Product
from products.permissions import IsStaffOrReadOnly
from products.serializers import ProductSerializers
from rest_framework import viewsets, filters


class CustomPagination(PageNumberPagination):
    page_size = 3


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    pagination_class = CustomPagination  # api/products/?page=2

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filter_class = ProductFilter
    search_fields = ['name', 'description']

    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category', None)
        if category:
            self.queryset = self.queryset.filter(category=category)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_products = Product.objects.filter(category=instance.category).exclude(id=instance.id)[:5]
        related_serializers = ProductSerializers(related_products, many=True)
        return Response({
            'product': serializer.data,
            'related_products': related_serializers.data
        })

    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        top_products = Product.objects.annotate(avg_rating=models.Avg('reviews__rating')).order_by('-avg_rating')[:2]
        serializers = ProductSerializers(top_products, many=True)
        return Response(serializers.data)

    @action(detail=True, methods=['get'])
    def avg_rating(self, request, pk=None):
        product = self.get_object()
        reviews = product.review.all()

        if reviews.count() == 0:
            return Response({'average_rating: No reviews yet!'})

        avg_rating = sum([review.rating for review in reviews]) / reviews.count()
        return Response({'average_rating:', avg_rating})
