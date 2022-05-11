from django.urls import path
from django.urls import path, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
app_name = 'customers'

urlpatterns = [
    path('home/<str:home_lat>/<str:home_long>/', views.Home, name="home"),
    path('', views.FirstHome, name="firstgome"),
    path('addtocart/<uuid:uuid_id>/', views.AddtoCart, name="addtocart"),
    path('removecart/<uuid:uuid_id>/', views.RemoveCart, name="removecart"),
    path('cartbill/<str:quantity>/', views.CartBill, name="cartbill"),
    path('paynow/', views.PayNow, name="paynow"),
    path('login/', views.Logins, name="login"),
    path('register/', views.Registers, name="register"),
    path('orders/', views.Orders, name="Orders"),
    path('cart/', views.Cart, name = "cart"),
    path('Phoneverify/', views.Phoneverify, name="Phoneverify"),
    path('OtpVerify/', views.OtpVerify, name="Otp"),
    path('customerproducts/<uuid:uuid_id>/', views.Products, name ="products"),
    path('specificcat/<uuid:uuid_id>/', views.SpecificCategory, name="specificcat"),
    path('customerproduct/<uuid:uuid_id>/', views.Product, name ="product"),
    path('currentloc/<str:str_lat>/<str:str_long>/', views.CurrentLoc, name="curloc"),
    path('mobileverify/', views.MobileVerify, name="mobileverify"),
    path('specificshop/<uuid:uuid_id>/', views.SpecificShop, name="specificshop"),
    path('shops/', views.Shops, name="shop"),
    path('deliveryoption/', views.DeliveryOption, name="deliveryoption"),
    re_path(r'^payment/(?P<p>.*)$', views.PaymentVerifyRequest),
    path('cashondeliver/', views.CashOnDeliveryRequest, name="cashonedelivery"),
    path('logout/', views.LogOut, name="logout"),
    path('shopsearch/', views.ShopSearch, name="shopsearch"),
    path('productsearch/', views.ProductSearch, name="productsearch"),
    path('shopnotfiund/', views.ShopNotFound, name="shopnotfound")
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# else:
#     urlpatterns += staticfiles_urlpatterns()