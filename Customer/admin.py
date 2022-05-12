from django.contrib import admin
from . import models


admin.site.register(models.CustomerUsers)
admin.site.register(models.CustomerImages)
admin.site.register(models.CustomerCart)
admin.site.register(models.CustomerOrders)
admin.site.register(models.CustomerAddress)
admin.site.register(models.CustomerProducts)
admin.site.register(models.FeedBack)

