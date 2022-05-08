import uuid
from django.db import models
from django.utils.timezone import now

class ShopsCategories(models.Model):
    Shops_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ProductsCategories(models.Model):
    name = models.CharField(max_length=200)
    categories_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop_id = models.ForeignKey(ShopsCategories, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Products(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    categories_id = models.ForeignKey(ProductsCategories, on_delete=models.CASCADE)
    name = models.TextField()
    specifications = models.TextField()
    descriptions = models.TextField()
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.name


class AllPayments(models.Model):
    nap_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_id = models.CharField(max_length=200)
    payment_status = models.CharField(max_length=100)
    payment_request_id = models.CharField(max_length=200)
    user_id = models.UUIDField()
    amount_paid = models.CharField(max_length=200)
    on_date = models.DateTimeField(default=now)

