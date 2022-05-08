from django.contrib import admin
from . import models

admin.site.register(models.ShopsCategories)
admin.site.register(models.ProductsCategories)
admin.site.register(models.Products)
admin.site.register(models.AllPayments)

