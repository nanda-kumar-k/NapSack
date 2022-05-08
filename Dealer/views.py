from django.shortcuts import render,HttpResponse, redirect

from Agents.models import AgentOrdersProducts, AgentOrders, AgentsUsers, AgentLocation
from Customer.models import CustomerOrders, CustomerUsers
from . import forms
from Agents.AgentsFunctions import password_check, phone_verify
# Create your views here.
from . import models
from django.contrib import messages
import datetime
from .models import DealerUsers

dealer_currentuser =""

def home(request):
    return render(request, 'layout/dealer_base.html' )



def DealerRegister(request):
    if request.method == "POST":
        form = forms.DRegistration(request.POST)
        pcheck = password_check(request.POST['password'])
        pnum = request.POST['phone_number']
        if pcheck == "correct":
            if phone_verify(pnum):
                if form.is_valid():
                    form.save()
                    check = models.DealerUsers.objects.filter(username=request.POST['username']).values()
                    global dealer_currentuser
                    temp = check[0]
                    dealer_currentuser = temp['dealer_user_id']
                    messages.success(request, f"New account created:")
                    # return render(request, "maps/Shop_location.html")
                    return redirect('dealers:dearlerlogin')
                else:
                    # form = forms.ALogin()
                    messages.error(request, f" UserName already exit...! Try Again  ")
                    # AgentsMessages.my_view(request,f" UserName already exit...! Try Again  ")
                    return render(request, "pages/dealer_register.html", {'form': form})
            else:
                messages.warning(request, f" Invalid Phone Number..! please include country code eg:+91  ")
                return render(request, "pages/dealer_register.html", {'form': form})

        else:
            # form = forms.ALogin()
            messages.warning(request, f" {pcheck} ")
            return render(request, "pages/dealer_register.html", {'form': form})
    else:
        form = forms.DRegistration()
    return render(request, "pages/dealer_register.html", {'form': form})




def DealerLogin(request):
    if request.method == "POST":
        user = request.POST['username']
        pwd = request.POST['password']
        check = models.DealerUsers.objects.filter(username=user, password=pwd).values()
        if check:
            global dealer_currentuser
            temp = check[0]
            dealer_currentuser = temp['dealer_user_id']
            # return redirect('agents:AgentsHomePage')
            return redirect('dealers:home')
        else:
            form = forms.DLogin()
            messages.info(request, f"Invalid UserName and Password...! Try Again ")
            return render(request, "pages/dealer_login.html", {'form': form})
    else:
        form = forms.DRegistration()
    return render(request, "pages/dealer_login.html", {'form': form})


def DealerOrders(request):
    d = models.DealerOrders.objects.filter(username=dealer_currentuser).order_by('oder_date').values()
    data = []
    j = 1
    for i in d:
        temp = i
        temp['sno'] = j
        if i['dealer_status']:
            temp['delivery_status'] = "delivery send"
        else:
            temp['delivery_status'] = "delivery not send"
        data.append(temp)
        j = j + 1
    return render(request, 'pages/dealer_orders.html', {'data': data})


def DealerOrderDetails(request, uuid_id):
    pro_data = AgentOrdersProducts.objects.filter(agentorders_id=uuid_id).values()
    co = CustomerOrders.objects.filter(order_id=uuid_id).values()
    co_one = co[0]
    cu = CustomerUsers.objects.filter(user_id=co_one['customerusername_id']).values()
    cu_one = cu[0]
    ao = AgentOrders.objects.filter(agent_order_id=uuid_id).values()
    ao_one = ao[0]
    du = AgentsUsers.objects.filter(agen_user_id=ao_one['agentsusers_id']).values()
    du_one = du[0]
    aloc = AgentLocation.objects.filter(username=ao_one['agentsusers_id']).values()
    aloc_one = aloc[0]
    user_data = {
        'order_id': uuid_id,
        'cname': cu_one['name'],
        'cphone': cu_one['phone_number'],
        'delivery_date': co_one['delivery_date'],
        'aname': du_one['first_name'] + du_one['last_name'],
        'aphone': du_one['phone_number'],
        'cost': co_one['bill'],
        'no_of_items': len(pro_data),
        'clong': co_one['longitude'],
        'clat': co_one['latitude'],
        'along' :aloc_one['longitude'],
        'alat' : aloc_one['latitude']
    }
    data = {
        'pro_data': pro_data,
        'user_data': user_data
    }
    return render(request, 'pages/dealer_order_details.html', {'data': data})


def DealerDirctions(request, long_id, lat_id):
    loc_data = str(long_id) + "," + str(lat_id)
    return render(request, 'dealer_maps/dealer_directions.html', {'data': loc_data})
def DealerOrderConformation(request, uuid_id):
    do = models.DealerOrders.objects.get(order_id=uuid_id)
    do.dealer_status = True
    current_time = datetime.datetime.now()
    y,m,d,h,mi, = current_time.year, current_time.month,current_time.day,current_time.hour,current_time.minute

    do.status = "Order Deliver on"+ " "  + str(y)+ ":"+str(m)+ ":"+str(d)+ ","+str(h)+ ":"+str(mi)
    ao = AgentOrders.objects.get(agent_order_id=uuid_id)
    ao.delivery_info = "Order Deliver on"+ " " + str(y)+ ":"+str(m)+ ":"+str(d)+ ","+str(h)+ ":"+str(mi)
    uo = CustomerOrders.objects.get(order_id=uuid_id)
    uo.status = "Deliver on "+ " " + str(y)+ ":"+str(m)+ ":"+str(d)+ ","+str(h)+ ":"+str(mi)
    do.save()
    ao.save()
    uo.save()
    return redirect('dealers:dearlerorders')


def DealerShopsVerification(request):
    data = models.DealerShopsVerifications.objects.filter(username=dealer_currentuser).order_by('date').values()
    final_data = []
    for d in data:
        cl = AgentLocation.objects.filter(username=d['agent_location_id']).values()
        cl_one = cl[0]
        cu = AgentsUsers.objects.filter(agen_user_id=cl_one['username_id']).values()
        temp = d
        cu_one = cu[0]
        temp['shopname']= cu_one['agent_shop_name']
        temp['along']= cl_one['longitude']
        temp['alat'] = cl_one['latitude']
        temp['agent_user_id'] = cl_one['username_id']
        final_data.append(temp)
    return render(request, 'pages/verify_shops.html', {'data':final_data})


def ShopVerify(request, uuid_id):
    ds = models.DealerShopsVerifications.objects.get(username_id=dealer_currentuser, agent_location= uuid_id)
    ds_find = models.DealerShopsVerifications.objects.filter(username_id=dealer_currentuser,
                                                             agent_location=uuid_id).values()
    us = AgentsUsers.objects.get(agen_user_id=uuid_id)
    ds_find_one = ds_find[0]
    if ds_find_one['verify_status']:
        ds.verify_status = False
        us.agent_verification = False
    else:
        ds.verify_status = True
        us.agent_verification = True
    ds.save()
    us.save()
    return redirect('dealers:shopsverification')


def DealerDailyUpdate(request,str_value):
    if str_value == "yes":
        return render(request, 'dealer_maps/dealer_current_location.html')
    elif str_value == "no":
        Dl_find = models.DealertLocation.objects.filter(username=dealer_currentuser).values()
        if Dl_find:
            Dl_user = models.DealertLocation.objects.get(username=dealer_currentuser)
            Dl_user.dealer_status = False
            Dl_user.save()
        return HttpResponse("okk done ")
    return render(request, 'pages/daily_update.html')


def DealerCurrentLocation(request,str_lat,str_long):
    Dl_find = models.DealertLocation.objects.filter(username=dealer_currentuser).values()
    print(Dl_find)
    if Dl_find:
        Dl_user = models.DealertLocation.objects.get(username=dealer_currentuser)
        Dl_user.longitude= str_long
        Dl_user.latitude = str_lat
        Dl_user.dealer_status = True
        Dl_user.save()
        return HttpResponse("okk update done")
    else:
        print("sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
        print(dealer_currentuser)
        Dl_get = models.DealerUsers.objects.get(dealer_user_id=dealer_currentuser)
        Dl_user = models.DealertLocation(username=Dl_get, longitude=str_long, latitude= str_lat,dealer_status=True)
        Dl_user.save()
        return HttpResponse("okk update done")
    return render(request, 'dealer_maps/dealer_current_location.html')





# insert the data

    # m = models.Members(firstname="adil", lastname="k")
    # m.save()
    # print(m)
    # k or kumar


    # geting all fileds with the list of dist

    # m = models.Members.objects.all().values()
    # print(m)
    # {'id': 1, 'firstname': 'nanda', 'lastname': 'k'}, {'id': 2, 'firstname': 'kumar', 'lastname': 'k'},]


    # to delete the rows

    # member = models.Members.objects.get(id=1)
    # member.delete()
    # print(models.Members.objects.all().values())


    # to update the recodes

    # member = models.Members.objects.get(id=2)
    # member.firstname = "first"
    # member.lastname = "last"
    # member.save()
    # print(models.Members.objects.all().values())


    # to get all list of objects

    # mydata = models.Members.objects.all()
    # print(mydata)
    #
    # list of objects <QuerySet [<Members: last>, <Members: k>]>


    # to get list of all values in the form of dist

    # mydata = models.Members.objects.all().values()


    # to get one column values


    # mydata = models.Members.objects.values_list('firstname').values()
    # print(mydata)
    # list with tuples <QuerySet [('first',), ('adil',)]>


    # to get specific row

    # mydata = models.Members.objects.filter(firstname='adil').values()
    # mydata = models.Members.objects.filter(lastname='Refsnes', id=2).values()
    # mydata = Members.objects.filter(firstname='Emil').values() | Members.objects.filter(firstname='Tobias').values()
    # .filter(firstname__startswith='L');
    # out will be list with dist


    # order by
    # ass mydata = Members.objects.all().order_by('firstname').values()
    # dess mydata = Members.objects.all().order_by('-firstname').values()
    # Multiple Order Bys
    # mydata = Members.objects.all().order_by('lastname', '-id').values()

    # all_category = models.ProductsCategories.objects.filter(shop_id="0210204445e14f4395a6042a914641e9").order_by('name').values()
    # print(all_category)

    # all_category = models.Products.objects.filter(categories_id="4987137b-8f52-44f4-b59f-368846c65133")
    # print(all_category)

    # return HttpResponse("<h1>welcome</h1>")