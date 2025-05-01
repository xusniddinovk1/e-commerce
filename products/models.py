from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    objects = None
    name = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    objects = None
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.CharField(max_length=155, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    data_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    objects = None
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product} - {self.rating}'
