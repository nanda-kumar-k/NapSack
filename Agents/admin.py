from django.contrib import admin
from . import models

admin.site.register(models.AgentsUsers)
admin.site.register(models.AgentProducts)
admin.site.register(models.AgentOrders)
admin.site.register(models.AgentOrdersProducts)
admin.site.register(models.Members)
admin.site.register(models.AgentShopCategorie)
admin.site.register(models.AgentLocation)


