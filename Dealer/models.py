from django.db import models
import uuid
from django.utils.timezone import now
# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField
from Agents.models import AgentOrders, AgentLocation
from Customer.models import CustomerOrders


class DealerUsers(models.Model):
    full_name = models.CharField(max_length=30)
    username = models.CharField(max_length=40, unique=True)
    dealer_user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    phone_number = PhoneNumberField( null=False, blank=False)
    created_on = models.DateTimeField(default=now)
    dealer_verification = models.BooleanField(default=False)
    image = models.ImageField(upload_to='dealer', default='images/shop.jpeg')

    def __str__(self):
        return self.username


class DealertLocation(models.Model):
    username = models.OneToOneField(DealerUsers, on_delete=models.CASCADE, primary_key=True,)
    longitude = models.CharField(max_length=100, default=None)
    latitude = models.CharField(max_length=100, default=None)
    date = models.DateTimeField(default=now)
    dealer_status = models.BooleanField(default=False)


class DealerOrders(models.Model):
    order_id = models.UUIDField(primary_key=True)
    oder_date = models.DateTimeField(default=now)
    status = models.TextField()
    dealer_status = models.BooleanField(default=False)
    username = models.ForeignKey(DealerUsers, on_delete=models.CASCADE)
    agent_order_id = models.ForeignKey(AgentOrders, on_delete=models.CASCADE)
    customer_order_id = models.ForeignKey(CustomerOrders, on_delete=models.CASCADE)
    delivery_date = models.DateTimeField(default=now)


class DealerShopsVerifications(models.Model):
    username = models.ForeignKey(DealerUsers, on_delete=models.CASCADE)
    date = models.DateTimeField(default=now, )
    verification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent_location = models.ForeignKey(AgentLocation,on_delete=models.CASCADE)
    verify_status = models.BooleanField(default=False)