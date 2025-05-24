from django_filters import rest_framework as django_filters
from products.models import Product


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='min_price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='max_price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price']
