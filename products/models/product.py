from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


class Category(models.Model):
    objects = None
    name = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    DoesNotExist = None
    objects = None
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.CharField(max_length=155, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    data_posted = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock > 0

    def reduce_stock(self, quantity):
        if quantity > self.stock:
            return False
        self.stock -= quantity
        self.save()
        return True

    def increase_stock(self, amount):
        self.stock += amount
        self.save()

    class Meta:
        ordering = ['name']