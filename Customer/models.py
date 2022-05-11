import email
from email import message
from email.mime import image
import uuid
from django.utils.timezone import now
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Address(models.Model):
    name = models.CharField(max_length=50)
    phone_number = PhoneNumberField( null=False, blank=False)
    pincode = models.PositiveIntegerField()
    locality = models.TextField()
    address = models.TextField()
    city_district_town = models.CharField(max_length=200)
    state = models.CharField(max_length=100)

    class Meta:
        abstract = True


class CustomerUsers(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=40, unique=True)
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    phone_number = PhoneNumberField( null=False, blank=False)
    created_on = models.DateTimeField(default=now)
    phone_verify = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class CustomerCart(models.Model):
    customerusername = models.ForeignKey(CustomerUsers, on_delete=models.CASCADE)
    shop_id = models.UUIDField()
    product_id = models.UUIDField()
    date = models.DateTimeField(default=now)




class CustomerAddress(Address):
    customerusername = models.ForeignKey(CustomerUsers, on_delete=models.CASCADE)

    def __str__(self):
        return self.customerusername


class CustomerOrders(models.Model):
    order_id = models.UUIDField(primary_key=True)
    oder_date = models.DateTimeField(default=now)
    payment_id = models.CharField(max_length=200)
    status = models.TextField()
    bill = models.CharField(max_length=100)
    customerusername = models.ForeignKey(CustomerUsers, on_delete=models.CASCADE)
    delivery_date = models.DateTimeField(default=now)
    longitude = models.CharField(max_length=100, default=None)
    latitude = models.CharField(max_length=100, default=None)
    payment_mode = models.CharField(max_length=200, default=None)



class CustomerProducts(models.Model):
    customer_product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    Categorie = models.CharField(max_length=200)
    cost = models.IntegerField()
    quantity = models.PositiveSmallIntegerField()
    customerorders = models.ForeignKey(CustomerOrders, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', default="customer_products.jpg")


class FeedBack(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    user = models.UUIDField()
    
    def __str__(self):
        return self.name






