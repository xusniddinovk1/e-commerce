from django.contrib import admin
from products.models import Category, Product, Order, Review

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Review)
