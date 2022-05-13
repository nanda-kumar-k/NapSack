from django.shortcuts import render, HttpResponse, redirect
from Customer import shopsearch

from Customer.cartfunctions import finddealer
from . import forms
from . import models
from NapsackAdmin.models import ProductsCategories, Products as NapProducts, ShopsCategories
from Customer.models import CustomerOrders, CustomerProducts, CustomerUsers
from Dealer.models import DealerOrders, DealerUsers, DealerShopsVerifications
from django.contrib import messages
from . import AgentsMessages
from . import AgentsFunctions

currentuser = ""
agent_long = ""
agent_lat = ""

def AgentsRegister(request):
    if request.method == "POST":
        form = forms.ALogin(request.POST)
        print(form.errors)
        pcheck = AgentsFunctions.password_check(request.POST['password'])
        pnum = request.POST['phone_number']
        if pcheck == "correct":
            if AgentsFunctions.phone_verify(pnum):
                print("checjjjjjjjjjjjj")
                if form.is_valid():
                    form.save()
                    check = models.AgentsUsers.objects.filter(username=request.POST['username']).values()
                    global currentuser
                    temp = check[0]
                    currentuser = temp['agen_user_id']
                    messages.success(request, f"New account created:")

                    return render(request, "maps/Shop_location.html")
                else:
                    # form = forms.ALogin()
                    messages.error(request, f" UserName already exit...! Try Again  ")
                    # AgentsMessages.my_view(request,f" UserName already exit...! Try Again  ")
                    return render(request, "pages/agentsregister.html", {'form': form})
            else:
                messages.warning(request, f" Invalid Phone Number..! please include country code eg:+91  ")
                return render(request, "pages/agentsregister.html", {'form': form})

        else:
            # form = forms.ALogin()
            messages.warning(request, f" {pcheck} ")
            return render(request, "pages/agentsregister.html", {'form': form})
    else:
        form = forms.ALogin()
    return render(request, "pages/agentsregister.html", {'form': form})


def ShopLoction(request,str_lat,str_long):
    print(currentuser)
    us = models.AgentsUsers.objects.get(agen_user_id=currentuser)
    s = models.AgentLocation(username=us,longitude=str_long,latitude=str_lat)
    s.save()
    global agent_long, agent_lat
    agent_long = str_long
    agent_lat = str_lat
    return redirect('agents:selectcategory')
    # data = ShopsCategories.objects.all().values()
    # print(type(data))
    # print(data)
    # return render(request, 'pages/selectcategory.html', {'data': data})


def AgentsLogin(request):
    if request.method == "POST":
        user = request.POST['username']
        pwd = request.POST['password']
        check = models.AgentsUsers.objects.filter(username=user, password=pwd).values()
        if check:
            check_one = check[0]
            if check_one['agent_verification']:
                global currentuser
                temp = check[0]
                currentuser = temp['agen_user_id']
                print(currentuser)
                return redirect('agents:AgentsHomePage')
            else:
                return HttpResponse("shop not verified ")

        else:
            form = forms.ALogin()
            messages.info(request, f"Invalid UserName and Password...! Try Again ")
            return render(request, "pages/agentslogin.html", {'form': form})
    else:
        form = forms.ALogin()
    return render(request, "pages/agentslogin.html", {'form': form})


def SelectCategory(request):
    data = ShopsCategories.objects.all().values()
    print(type(data))
    print(data)
    return render(request, 'pages/selectcategory.html',{'data': data})


def AddCategory(request, uuid_id):
    print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
    print(uuid_id)
    us = models.AgentsUsers.objects.get(agen_user_id=currentuser)
    ct = ShopsCategories.objects.get(Shops_id=uuid_id)
    s = models.AgentShopCategorie(username=us,agent_shop_categorie=ct)
    s.save()
    dlr = finddealer(agent_lat, agent_long)
    d = dlr[0]
    dlr_one = d['username_id']
    print("ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
    print(dlr_one)
    ag_loc = models.AgentLocation.objects.get(username=currentuser)
    dlr_get = DealerUsers.objects.get(dealer_user_id=dlr_one)
    dealer = DealerShopsVerifications(username=dlr_get, agent_location=ag_loc)
    dealer.save()
    return redirect('agents:AgentsLogin')


def AgentsHome(request):
    return render(request, "layout/base.html")


def Orders(request):
    d = models.AgentOrders.objects.filter(agentsusers=currentuser).order_by('order_date').values()
    data = []
    j = 1
    for i in d:
        temp = i
        temp['sno'] = j
        if i['delivery_status']:
            temp['delivery_status'] = "delivery send"
        else:
            temp['delivery_status'] = "delivery not send"
        data.append(temp)
        j = j+1
    return render(request, "pages/orders.html", {'data': data})


def OrderDetails(request, uuid_id):
    pro_data =  models.AgentOrdersProducts.objects.filter(agentorders_id=uuid_id).values()
    co = CustomerOrders.objects.filter(order_id= uuid_id).values()
    co_one = co[0]
    cu = CustomerUsers.objects.filter(user_id=co_one['customerusername_id']).values()
    cu_one = cu[0]
    Do = DealerOrders.objects.filter(order_id=uuid_id).values()
    Do_one = Do[0]
    du = DealerUsers.objects.filter(dealer_user_id=Do_one['username_id']).values()
    du_one =  du[0]
    user_data = {
        'order_id' :uuid_id,
        'cname': cu_one['name'],
        'cphone':cu_one['phone_number'],
        'delivery_date': co_one['delivery_date'],
        'dname': du_one['full_name'],
        'dphone': du_one['phone_number'],
        'cost': co_one['bill'],
        'no_of_items': len(pro_data),
    }
    data = {
        'pro_data': pro_data,
        'user_data': user_data
    }
    return render(request, "pages/orderdetails.html", {'data': data})


def ProductsCheck(uuid_id):
    all_products = models.Products.objects.filter(categories_id=uuid_id).values()
    products = models.AgentProducts.objects.filter(agentsusers=currentuser).values()
    # print(all_products)
    # print(products)
    productdata = []

    for apr in all_products:
        products = models.AgentProducts.objects.filter(agentsusers=currentuser,product_id_id=apr['product_id'] ).values()
        if products:
            continue
        else:
            productdata.append(apr)

    agent_categories = models.AgentShopCategorie.objects.filter(username=currentuser).values()
    tac = agent_categories[0]
    tac_id = tac['agent_shop_categorie_id']
    all_categories = models.ProductsCategories.objects.filter(shop_id=tac_id).order_by(
        'name').values()
    print("llllllllllllllllllllllllllllllll")
    print(len(productdata))

    data = {
        'categories': all_categories,
        'products': productdata,
    }
    return data


def AddProductsInfo(request):
    agent_categories = models.AgentShopCategorie.objects.filter(username=currentuser).values()
    print(agent_categories)
    tac = agent_categories[0]
    print(tac)
    tac_id = tac['agent_shop_categorie_id']
    print(tac_id)
    all_categories = models.ProductsCategories.objects.filter(shop_id=tac_id).order_by(
        'name').values()
    print(all_categories)
    t1c = all_categories[0]
    t1cid = t1c['categories_id']
    data = ProductsCheck(t1cid)
    print("rgggggggggggggggggggggggggggggghdzhf;siuhnskjb;Adjjjjjjjjjjjjjjjjjjjjjjjjjskd>djdsfnsjnskjnskgvnrsknfwsf")
    print(type(data))
    for i in data:
        print(i)
    print(data)
    return render(request, "pages/addproducts.html", {'data': data})



def AddProducts(request, uuid_id):

    if request.method == "POST":
        Icost = request.POST['cost']
        Ioffer = request.POST['offer']
        Inoofitemspresent = request.POST['noofitemspresent']
        us = models.AgentsUsers.objects.get(agen_user_id=currentuser)
        pt = NapProducts.objects.get(product_id=uuid_id)
        find_cat = NapProducts.objects.filter(product_id=uuid_id).values()
        find_cat_one = find_cat[0]
        f_get = ProductsCategories.objects.get(categories_id=find_cat_one['categories_id_id'])
        f_cat_name = ProductsCategories.objects.filter(categories_id=find_cat_one['categories_id_id']).values()
        f_cat_name_one = f_cat_name[0]
        m = models.AgentProducts(agentsusers=us,product_id=pt, cost=Icost, offer=Ioffer,
                             quantity_present=Inoofitemspresent, Categories_name=f_cat_name_one['name'],categories=f_get)
        m.save()

        return redirect('agents:Agentsaddproductsinfo')
    else:
        data = ProductsCheck(uuid_id)
        return render(request, "pages/addproducts.html", {'data': data})



def UpdateProductCheck():
    products_agent = models.AgentProducts.objects.filter(agentsusers=currentuser).values()
    print(type(products_agent))
    data = []
    for pro in products_agent:
        temp = pro
        products_admin = models.Products.objects.filter(product_id=pro['product_id_id']).values()
        nap_product = NapProducts.objects.get(product_id=pro['product_id_id'])
        tp1 = products_admin[0]
        temp['name'] = tp1['name']
        temp['img'] = nap_product
        categories_admin = models.ProductsCategories.objects.filter(categories_id=tp1['categories_id_id']).values()
        tc1 = categories_admin[0]
        temp['categories_id'] = tc1['name']
        data.append(temp)
    return data


def Products(request):
    if request.method == "POST":
        pattern = request.POST['search']
        all_products = UpdateProductCheck()
        q = 3
        data = []
        for oneshop in all_products:
            if shopsearch.search(pattern, oneshop['name'].lower(), q) :
                data.append(oneshop)
        if data:
            return render(request, "pages/products.html", {'productsdata': data})
        else:
            messages.error(request, 'No Products Found')
            return render(request, "pages/products.html", {'productsdata': data})
    data = UpdateProductCheck()
    return render(request, "pages/products.html", {'productsdata': data})

    

def Productsupdate(request, uuid_id):
    if request.method == "POST":
        Icost = request.POST['cost']
        Ioffer = request.POST['offer']
        Inoofitemspresent = request.POST['noofitemspresent']
        update = models.AgentProducts.objects.get(agent_product_id=uuid_id)
        update.cost = Icost
        update.offer = Ioffer
        update.quantity_present = Inoofitemspresent
        update.save()
        data = UpdateProductCheck()
        return render(request, "pages/products.html", {'productsdata': data})
    else:
        data = UpdateProductCheck()
        newdata = []
        for pro in data:
            if pro['agent_product_id'] == uuid_id:
                newdata.append(pro)
    return render(request, "pages/updateproduct.html", {'productsdata': newdata})


def ProductRemove(request, uuid_id):
    pr = models.AgentProducts.objects.get(agent_product_id=uuid_id)
    pr.delete()
    return redirect('agents:Agentsproducts')

















def example(request):
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
    return render(request, "pages/updateproduct.html")
