import email
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from . import shopsearch

from Customer.shopsearch import search
from . import forms
from Agents.AgentsFunctions import phone_verify, password_check
from . import models
from django.contrib import messages
import random
import requests
from django.shortcuts import redirect, reverse
from  . import locationfunctions
from Agents.models import AgentShopCategorie, AgentProducts, AgentsUsers
from NapsackAdmin.models import ShopsCategories,Products as Napproducts,ProductsCategories
from . import payments
from . import cartfunctions
import random
currentuser = ""
mnumber = ""
lat = "16.439135"
long = "80.624908"
# lat = ""
# long = ""
shopid = ""
cart_bill_data = []
sp = ""


def Phoneverify(request):
    if request.method == 'POST':
        po = request.POST['phone']
        otp = random.randint(1000, 9999)
        x = requests.request("GET", f'https://2factor.in/API/V1/df1606dc-a515-11ec-a4c2-0200cd936042/SMS/{po}/{otp}/NapSack')
        s = x.json()
        # global temp
        # temp = otp
        if s['Status'] == "Success":
            return redirect(reverse('Otp'))
        else:
            return HttpResponse("<h1>try again</h1>")

    return render(request, "forms/PhoneVerify.html")


def OtpVerify(request):
    # if request.method == 'POST':
    #     otp = request.POST['otp']
    #     if otp == str(temp):
    #         return redirect(reverse('Register'))
    #     else:
    #         return HttpResponse("<h1>wrong</h1>")
    return render(request, "forms/otpverify.html")

votp = 0
def MobileVerify(request):
    global votp
    if request.method == 'POST':
        v1 = request.POST['v1']
        v2 = request.POST['v2']
        v3 = request.POST['v3']
        v4 = request.POST['v4']
        v5 = request.POST['v5']
        otp = v1+v2+v3+v4+v5
        if otp == str(votp):
            return redirect('customers:login')
        else:
            return HttpResponse("<h1>wrong</h1>")
    else:
        otp = random.randint(10000, 99999)
        x = requests.request("GET",f'https://2factor.in/API/V1/df1606dc-a515-11ec-a4c2-0200cd936042/SMS/{mnumber}/{otp}/NapSack')
        s = x.json()
        votp = otp
        if s['Status'] == "Success":
            return render(request, 'pages/MobileVerify.html')
        else:
            return HttpResponse("<h1>try again</h1>")



def Registers(request):
    if request.method == "POST":
        form = forms.CRegistration(request.POST, request.FILES)
        print(form.errors)
        pcheck = password_check(request.POST['password'])
        pnum = request.POST['phone_number']
        if pcheck == "correct":
            if phone_verify(pnum):
                print("checjjjjjjjjjjjj")
                if form.is_valid():
                    form.save()
                    global mnumber
                    mnumber = pnum
                    messages.success(request, f"New account created:")
                    # return redirect('customers:mobileverify')
                    return redirect('customers:login')
                else:
                    # form = forms.ALogin()
                    messages.error(request, f" UserName already exit...! Try Again  ")
                    # AgentsMessages.my_view(request,f" UserName already exit...! Try Again  ")
                    return render(request, "pages/customer_register.html", {'form': form})
            else:
                messages.warning(request, f" Invalid Phone Number..! please include country code eg:+91  ")
                return render(request, "pages/customer_register.html", {'form': form})

        else:
            # form = forms.ALogin()
            messages.info(request, f" {pcheck} ")
            return render(request, "pages/customer_register.html", {'form': form})
    else:
        form = forms.CRegistration()
    return render(request, "pages/customer_register.html", {'form': form})


def Logins(request):
    if request.method == "POST":
        user = request.POST['username']
        pwd = request.POST['password']
        check = models.CustomerUsers.objects.filter(username=user, password=pwd).values()
        if check:
            global currentuser, cart_bill_data
            temp = check[0]
            cart_bill_data = []
            currentuser = temp['user_id']
            models.CustomerCart.objects.filter(customerusername=currentuser).delete()
            # return redirect('customers:shop')
            return render(request, "maps/current_location.html")
        else:
            messages.error(request, f"Invalid UserName and Password...! Try Again ")
            return render(request, "pages/customer_Login.html")

    return render(request, "pages/customer_Login.html")


def Home(request, home_lat, home_long):
    # global lat, long
    # lat = home_lat
    # long = home_long
    d = locationfunctions.shoploc(lat, long)
    pro_data = []
    imgs = []
    for i in d:
        a_pro = AgentProducts.objects.filter(agentsusers=i['agent_id']).values()
        if a_pro:
            print(a_pro)
            find_l = len(a_pro)
            print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
            print(find_l)
            lis = [*range(0,find_l,1)]
            find = random.choice(lis)
            print(find)
            pro_one = a_pro[find]
            nap = Napproducts.objects.filter(product_id=pro_one['product_id_id']).values()
            nap_one = nap[0]
            a_pro_one = a_pro[0]
            nap_img = Napproducts.objects.get(product_id=pro_one['product_id_id'])
            temp = {
                'name': nap_one['name'],
                'cost' : a_pro_one['cost'],
                'offer' : a_pro_one['offer'],
                'img' : nap_img
            }
            pro_data.append(temp)
            imgs.append(nap_img)

    data = [d, imgs, pro_data]
    return render(request, "pages/home.html", {"data": data})

def FirstHome(request):
    return render(request, "pages/firsthome.html")

def LogOut(request):
    global currentuser, mnumber, lat, long, shopid, cart_bill_data
    models.CustomerCart.objects.filter(customerusername=currentuser).delete()
    currentuser = ""
    mnumber =  ""
    # lat = ""
    # long = ""
    shopid = ""
    cart_bill_data = []
    return redirect('customers:firstgome')


        
def FindCat():
    d = locationfunctions.shoploc(lat, long)
    temp1 = []
    temp = []
    for cname in d:
        if cname['name'] not in temp1:
            temp1.append(cname['name'])
            temp.append(cname)
    return temp

def ShopSearch(request):
    if request.method == "POST":
        pattern = request.POST['search']
        d = shopsearch.SearchFind(pattern, lat, long)
    else:
        d = []
    c = FindCat()
    data =[c,d]
    return render(request, "pages/shopsearch.html", {"data": data})

def Findshops(id):
    d = locationfunctions.shoploc(lat, long)
    shop_id = id
    if id == "fristshop":
        temp = d[0]
        shop_id = temp['agent_shop_categorie_id']
    data = []
    for sort_cat in d:
        if shop_id == sort_cat['agent_shop_categorie_id']:
            data.append(sort_cat)
    return data


def Shops(request):
    if currentuser or shopid or lat or long:
        redirect('customers:login')
    d = Findshops("fristshop")
    c = FindCat()
    data =[c,d]
    # return render(request, "pages/customer_shops.html", {'data':data})
    # return render(request, "pages/shopnotfound.html")
    return render(request, "pages/customer_forgot_password.html")


def SpecificShop(request, uuid_id):
    if currentuser or shopid or lat or long:
        redirect('customers:login')
    d = Findshops(uuid_id)
    c = FindCat()
    data = [c,d]
    return render(request, "pages/customer_shops.html", {'data': data})


def Orders(request):
    if currentuser or shopid or lat or long:
        redirect('customers:login')
    order_ass = models.CustomerOrders.objects.filter(customerusername=currentuser).order_by('oder_date').values()
    orderinfo = order_ass[::-1]
    data = []
    for oinfo in orderinfo:
        temp = {}
        t1 = oinfo
        user_info = models.CustomerUsers.objects.filter(user_id=currentuser).values()
        user_info_one = user_info[0]
        t1['name'] = user_info_one['name']
        t1['phone'] = user_info_one['phone_number']
        t1['email'] = user_info_one['email']
        orders_products = models.CustomerProducts.objects.filter(customerorders=oinfo['order_id']).values()
        temp_products = []
        for i in orders_products:
            img_url = models.CustomerProducts.objects.get(customer_product_id=i['customer_product_id'])
            t = i
            t['img'] = img_url
            temp_products.append(t)
        t1['no_of_items'] = len(orders_products)
        temp['order_info'] = t1
        temp['order_products'] = temp_products
        data.append(temp)
    return render(request, "pages/customer_orders.html", {'data':data})


def AddtoCart(request, uuid_id):
    if currentuser or shopid or lat or long:
        redirect('customers:login')
    un = models.CustomerUsers.objects.get(user_id=currentuser)
    # Auid = AgentShopCategorie.objects.filter(agent_shop_categorie_id=shopid).values()
    # uid_one = Auid[0]
    # Aun = uid_one['username_id']
    find =  models.CustomerCart.objects.filter(product_id=uuid_id).values()
    if find:
        return redirect('customers:products',shopid)  # redirect to products page
    else:
        s = models.CustomerCart(customerusername=un, shop_id=shopid, product_id=uuid_id)
        s.save()
        data = {
            'data' : shopid,
            'yorn' : True
        }
    return redirect('customers:products' , shopid) # redirect to products page

def RemoveCart(request, uuid_id):
    if currentuser or shopid or lat or long:
        redirect('customers:login')
    pro = models.CustomerCart.objects.get(product_id=uuid_id)
    pro.delete()
    return redirect('customers:cart')


def CartData():
    cartp = models.CustomerCart.objects.filter(customerusername=currentuser).order_by('date').values()
    data = []
    i = 1
    for p_one in cartp:
        temp_p = p_one
        Ap = AgentProducts.objects.filter(agentsusers=p_one['shop_id'], agent_product_id=p_one['product_id']).values()
        Ap_one = Ap[0]
        Np = Napproducts.objects.filter(product_id=Ap_one['product_id_id']).values()
        img_url = Napproducts.objects.get(product_id=Ap_one['product_id_id'])
        Np_one = Np[0]
        temp_p['nap_product_id'] = Np_one['product_id']
        temp_p['Categories_name'] = Ap_one['Categories_name']
        temp_p['product_name'] = Np_one['name']
        temp_p['img'] = img_url
        temp_p['Actual_cost'] = int(Ap_one['cost'])
        temp_p['offer'] = Ap_one['offer']
        temp_p['cost'] = int(Ap_one['cost'] - ((Ap_one['offer'] / 100) * Ap_one['cost']))
        q_temp = Ap_one['quantity_present']
        if q_temp >= 10:
            q_temp = 10
        temp_p['qty'] = range(1, q_temp + 1)
        temp_p['class_name'] = "c" + str(i)
        data.append(temp_p)
        i = i + 1
    print("carttttttttttttcartttttttttttttttttttttcartttttttttttttttttttttttt")
    print(len(data))
    return data


def Cart(request):
    if currentuser or shopid or lat or long:
        redirect('customers:login')
    data = CartData()
    print("44444444444444444444444444444444444444444444444444444444444444444444444444")
    print(len(data))
    return render(request, "pages/customer_cart.html", {'data':data})



def CartBill(request, quantity):
    if currentuser or shopid or lat or long:
        redirect('customers:login')
    d = CartData()
    global cart_bill_data
    cart_bill_data = []
    i = 3
    products_cost = 0
    for qt in d:
        temp_data = qt
        temp_data['qty_selected'] = quantity[i]
        products_cost = products_cost + (temp_data['cost'] * int(quantity[i]))
        cart_bill_data.append(temp_data)
        i = i + 1
    cart_bill_data.append(products_cost)
    # pay_url = payments.get_payment_url(products_cost, currentuser)
    userinfo = models.CustomerUsers.objects.filter(user_id=currentuser).values()
    userinfo_one = userinfo[0]
    # userinfo_one['pay_url'] = pay_url
    userinfo_one['cost'] = products_cost
    userinfo_one['total_items'] = len(d)
    total_data = {
        'cat_info' : d,
        'user_info' : userinfo_one
    }
    print("44444444444444444444444444444444444444444444444444444444444444444444444444")
    print(len(d))
    print("44444444444444444444444444444444444444444444444444444444444444444444444444")
    print(len(cart_bill_data))
    return render(request, 'pages/delivery_option.html', {'data':total_data})

def PayNow (request):
    l = len(cart_bill_data)
    pro_cost = cart_bill_data[l-1]
    pay_url = payments.get_payment_url(pro_cost , currentuser)
    return HttpResponseRedirect(pay_url)

def PaymentVerifyRequest(request,p):
    if currentuser or shopid or lat or long:
        redirect('customers:login')
    payment_id = request.GET['payment_id']
    payment_request_id = request.GET['payment_request_id']
    payment_status = request.GET['payment_status']
    if payments.verify_payment(payment_id,payment_request_id):
        payments.UpdatePayments(payment_id,payment_request_id,payment_status,currentuser,lat, long,cart_bill_data,shopid )
        # cartfunctions.updateorders(cart_bill_data,currentuser,shopid, lat, long)
        return HttpResponse("<h1>Payment Done</h1>")
    else:
        return HttpResponse("<h1>Contact NapSack People Payment not done</h1>")

    return HttpResponse(request.get_full_path)

def CashOnDeliveryRequest(request):
    if currentuser or shopid or lat or long:
        redirect('customers:login')
    cartfunctions.UpdateCOD(currentuser,lat, long,cart_bill_data,shopid)
    cart_bill_data.clear()
    return redirect('customers:Orders')



def ProductsCat():
    # print("productssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
    # Auid = AgentShopCategorie.objects.filter(agent_shop_categorie_id=shopid).values()
    # uid_one = Auid[0]
    # Aun = uid_one['username_id']
    # print(Aun)
    Apro = AgentProducts.objects.filter(agentsusers=shopid).values()
    print(Apro)
    data = []
    for each in Apro:
        print("nandandasadaffdsfsfjgfgliufgslfighslfgjkfgkdhiusghvksgkfhskuhskfhskjhsgfjlshgsdjgfjgskjfhgkfhisuhf")
        Cpro = models.CustomerCart.objects.filter(customerusername=currentuser, product_id=each['agent_product_id']).values()
        print("proooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
        print(Cpro)
        if Cpro:
            print("enterrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrwwwwwwwwwwwwwwwwwwwwwwww")
            continue
        else:
            p_temp = Napproducts.objects.filter(product_id=each['product_id_id']).values()
            img_url = Napproducts.objects.get(product_id=each['product_id_id'])
            p_temp_one = p_temp[0]
            c_temp = ProductsCategories.objects.filter(categories_id=p_temp_one['categories_id_id']).values()
            c_temp_one = c_temp[0]
            temp_data = each
            temp_data['categories_id'] = p_temp_one['categories_id_id']
            temp_data['categorie_name'] = c_temp_one['name']
            temp_data['product_name'] = p_temp_one['name']
            temp_data['offercost'] = int(each['cost'] - ((each['offer'] / 100) * each['cost']))
            temp_data['img'] = img_url
            data.append(temp_data)
    print("tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt")
    print(data)
    return data


def ProductsFilter(cat_id):
    data = []
    d = ProductsCat()
    temp_uuid = cat_id
    if cat_id == "firstone":
        temp_data = d[0]
        temp_uuid = temp_data['categories_id']
    for filt in d:
        if filt['categories_id'] == temp_uuid:
            data.append(filt)
    return data


def ProductsCatFilter():
    d = ProductsCat()
    temp1 = []
    temp = []
    for cname in d:
        if cname['categorie_name'] not in temp1:
            temp1.append(cname['categorie_name'])
            temp.append(cname)
    return temp

def Products(request, uuid_id):
    if currentuser or lat or long:
        redirect('customers:login')
    # if currentuser and shopid and lat and long:
    #     redirect('customers:login')
    global shopid
    shopid = uuid_id
    # Auid = AgentShopCategorie.objects.filter(agent_shop_categorie_id=uuid_id).values()
    # uid_one = Auid[0]
    # Aun = uid_one['username_id']
    # pll = AgentProducts.objects.filter(agentsusers=Aun).values()
    # print("ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
    # print(pll)
    d = ProductsFilter("firstone")
    c = ProductsCatFilter()
    data = [c, d]
    return render(request, 'pages/customer_products.html', {'data':data})


def ProductSearch(request):
    if request.method == "POST":
        pattern = request.POST['search']
        all_products = ProductsCat()
        q = 3
        d = []
        for oneshop in all_products:
            if shopsearch.search(pattern, oneshop['product_name'].lower(), q) :
                d.append(oneshop)
    else:
        d = []
    c = ProductsCatFilter()
    data =[c,d]
    return render(request, 'pages/customer_products.html', {'data':data})


def SpecificCategory(request, uuid_id):
    if currentuser or shopid or lat or long:
        redirect('customers:login')
    d = ProductsFilter(uuid_id)
    c = ProductsCatFilter()
    data = [c,d]
    global sp
    sp = uuid_id
    return render(request, 'pages/customer_products.html', {'data': data})


def Product(request, uuid_id):
    if currentuser or shopid or lat or long:
        redirect('customers:login')
    Auid = AgentShopCategorie.objects.filter(username_id=shopid).values()
    uid_one = Auid[0]
    Aun = uid_one['username_id']
    Apro = AgentProducts.objects.filter(agentsusers=Aun,agent_product_id=uuid_id ).values()
    Apro_one = Apro[0]
    data = []
    p_temp = Napproducts.objects.filter(product_id=Apro_one['product_id_id']).values()
    img_url = Napproducts.objects.get(product_id=Apro_one['product_id_id'])
    p_temp_one = p_temp[0]
    c_temp = ProductsCategories.objects.filter(categories_id=p_temp_one['categories_id_id']).values()
    c_temp_one = c_temp[0]
    Auser = AgentsUsers.objects.filter(agen_user_id=Aun).values()
    Auser_one = Auser[0]
    temp_data = Apro_one
    temp_data['shop_name'] = Auser_one['agent_shop_name']
    temp_data['categories_id'] = p_temp_one['categories_id_id']
    temp_data['categorie_name'] = c_temp_one['name']
    temp_data['product_name'] = p_temp_one['name']
    temp_data['image_id'] = p_temp_one['image']
    extra_word = p_temp_one['specifications']
    temp_data['specifications'] = extra_word.split("@")
    extra_word = p_temp_one['descriptions']
    temp_data['descriptions'] = extra_word.split("@")
    temp_data['Actual_cost'] = int(Apro_one['cost'])
    temp_data['offer'] = Apro_one['offer']
    temp_data['img'] = img_url
    temp_data['cost'] = int(Apro_one['cost'] - ((Apro_one['offer'] / 100) * Apro_one['cost']))
    q_temp = Apro_one['quantity_present']
    if q_temp >= 10:
        q_temp = 10
    temp_data['qty'] = range(1, q_temp + 1)
    data.append(temp_data)

    return render(request, 'pages/customer_product.html',{'data': data})


def CurrentLoc(request,str_lat,str_long):
    if currentuser:
        redirect('customers:login')
    # global lat, long
    # lat = str_lat
    # long = str_long
    return redirect('customers:shop')


def DeliveryOption(request):
    if currentuser or shopid or lat or long:
        redirect('customers:login')
    return render(request, 'pages/delivery_option.html')


def ShopNotFound(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        mssg = request.POST['message']
        form_save = models.FeedBack(name=name, email=email, phone_number=phone, message=mssg, user=currentuser)
        form_save.save()
        messages.success(request, f"Your form has been submitted successfully. We will get back to you soon.")
        return render(request, 'pages/shopnotfound.html')
    else:
        return render(request, 'pages/shopnotfound.html')
        
        