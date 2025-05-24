from django.contrib.auth import get_user_model
from .products import Category, Product
from django.core.validators import RegexValidator
from django.db import models

User = get_user_model()

phone_regex = RegexValidator(
    regex=r"^\+998\d{9}$",
    message='Phone numer must be in this format: +998123456789'
)


class Order(models.Model):
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELED = 'Cancelled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True, null=True)
    is_paid = models.BooleanField(default=False, null=True)

    def set_status(self, new_status):
        if new_status not in dict(self.STATUS_CHOICES):
            raise ValueError('Invalid Error')
        self.status = new_status
        self.save()

    def is_transition_allowed(self, new_status):
        allowed_transition = {
            self.PENDING: [self.PROCESSING, self.CANCELED],
            self.PROCESSING: [self.SHIPPED, self.CANCELED],
            self.SHIPPED: [self.DELIVERED, self.CANCELED],
        }
        return new_status in allowed_transition.get(self.status, [])

    def __str__(self):
        return f'{self.customer} ordered {self.product}'
