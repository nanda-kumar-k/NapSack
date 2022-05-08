import uuid
from django.utils.timezone import now
from Customer.models import Address,CustomerOrders
from NapsackAdmin.models import ProductsCategories, Products,ShopsCategories
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models


class AgentsUsers(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=40, unique=True)
    agen_user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    # phone_number = models.IntegerField()
    phone_number = PhoneNumberField( null=False, blank=False)
    created_on = models.DateTimeField(default=now)
    agent_shop_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    agent_shop_name = models.TextField()
    location = models.TextField()
    agent_verification = models.BooleanField(default=False)
    # shop_categorie = models.CharField(max_length=200)
    # agent_shop_categorie = models.ForeignKey(ShopsCategories, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', default="default.img")

    def __str__(self):
        return self.username


class AgentLocation(models.Model):
    username = models.OneToOneField(AgentsUsers, on_delete=models.CASCADE, primary_key=True, )
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    

class AgentShopCategorie(models.Model):
    username = models.OneToOneField(AgentsUsers, on_delete=models.CASCADE, primary_key=True,)
    agent_shop_categorie = models.ForeignKey(ShopsCategories, on_delete=models.CASCADE)


class AgentsAddress(models.Model):
    username = models.OneToOneField(AgentsUsers,on_delete=models.CASCADE,primary_key=True,)
    phone_number = models.PositiveIntegerField()
    pincode = models.PositiveIntegerField()
    locality = models.TextField()
    address = models.TextField()
    city_district_town = models.CharField(max_length=200)
    state = models.CharField(max_length=100)


# class AgentProductsCategories(models.Model):
#     name = models.CharField(max_length=200)
#     agent_shop_id = models.ForeignKey(AgentsUsers, on_delete=models.CASCADE)
#     Categories_name = models.CharField(max_length=300)
#     product_categories = models.ForeignKey(ProductsCategories, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name


class AgentProducts(models.Model):
    Categories_name = models.CharField(max_length=300,default=None)
    agentsusers = models.ForeignKey(AgentsUsers, on_delete=models.CASCADE)
    agent_product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    categories = models.ForeignKey(ProductsCategories, on_delete=models.CASCADE)
    cost = models.IntegerField()
    offer = models.IntegerField()
    quantity_present = models.IntegerField()

    # def __str__(self):
    #     return self.agent_product_id


class AgentOrders(models.Model):
    agentsusers = models.ForeignKey(AgentsUsers, on_delete=models.CASCADE)
    agent_order_id= models.UUIDField(primary_key=True)
    bill = models.CharField(max_length=100)
    delivery_info = models.TextField()
    order_date =  models.DateTimeField(default=now)
    delivery_date = models.DateTimeField(default=now)
    delivery_status = models.BooleanField(default=False)
    #
    # def __str__(self):
    #     return self.agentsusers


class AgentOrdersProducts(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agentorders = models.ForeignKey(AgentOrders, on_delete=models.CASCADE)
    name = models.TextField()
    Categorie = models.CharField(max_length=200)
    cost = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField()


    # def __str__(self):
    #     return self.name



#
#
# class AgentOrdersDelivered(Address):
#     agentsusers = models.ForeignKey(AgentsUsers, on_delete=models.CASCADE)
#     agent_order_delivered_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     customerorders_id = models.TextField()
#     bill = models.PositiveIntegerField()
#
#     def __str__(self):
#         return self.agentsusers
#
#
# class AgentOrdersDeliveredProducts(models.Model):
#     name = models.TextField()
#     Categorie = models.CharField(max_length=200)
#     cost = models.PositiveIntegerField()
#     delivery_status = models.CharField(max_length=200)
#     delivery_on = models.DateField()
#
#     def __str__(self):
#         return self.name
#

class Members(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)

    def __str__(self):
        return self.lastname