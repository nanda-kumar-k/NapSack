from django.urls import path
from . import views

app_name = 'dealers'

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.DealerLogin, name="dearlerlogin"),
    path('register/', views.DealerRegister, name="dearlerregister"),
    path('dealerdailyupdate/<str:str_value>/', views.DealerDailyUpdate, name="dealerdailyupdate"),
    path('dealerloc/<str:str_lat>/<str:str_long>/', views.DealerCurrentLocation, name="dealerloc"),
    path('orderdetails/<uuid:uuid_id>/', views.DealerOrderDetails, name="dealerorderdetails"),
    path('orders/', views.DealerOrders, name="dearlerorders"),
    path('directions/<str:long_id>/<str:lat_id>/', views.DealerDirctions, name="directions"),
    path('orderconfirmation/<uuid:uuid_id>/', views.DealerOrderConformation, name="orderconfirmation"),
    path('dealershopsverification/', views.DealerShopsVerification, name="shopsverification"),
    path('shopverify/<uuid:uuid_id>/', views.ShopVerify, name="shopverify")
]

