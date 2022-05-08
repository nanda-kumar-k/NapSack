from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.DealerUsers)
admin.site.register(models.DealertLocation)
admin.site.register(models.DealerOrders)
admin.site.register(models.DealerShopsVerifications)