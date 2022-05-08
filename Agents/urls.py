from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
app_name = 'agents'

urlpatterns = [
    path('', views.AgentsLogin, name="AgentsLogin"),
    path('agentsregister/',views.AgentsRegister, name="AgentsRegister"),
    path('agentshome/', views.AgentsHome,name="AgentsHomePage"),
    path('agentsorder/', views.Orders, name="AgentsOrders"),
    path('agentsorderdetails/<uuid:uuid_id>/', views.OrderDetails, name="Agentsorderdetails"),
    path('agentsaddproductsinfo/', views.AddProductsInfo, name="Agentsaddproductsinfo"),
    path('agentsaddproductsinfo/<uuid:uuid_id>/', views.AddProducts, name="Agentsaddproducts"),
    path('agentsproducts/', views.Products, name="Agentsproducts"),
    path('agentsproducts/<uuid:uuid_id>/', views.Productsupdate, name="Agentsproductupdate"),
    path('agentsproductsremove/<uuid:uuid_id>/', views.ProductRemove, name="Agentsproductremove"),
    path('<str:str_lat>/<str:str_long>/', views.ShopLoction, name="shoploc"),
    path('<uuid:uuid_id>/', views.AddCategory, name="addcategory"),
    path('selectcategory/', views.SelectCategory, name="selectcategory"),



    path('example/', views.example)
]



