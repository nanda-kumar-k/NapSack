from . import models
from Agents.models import AgentLocation, AgentOrders, AgentOrdersProducts, AgentProducts, AgentShopCategorie, AgentsUsers
import uuid
from Dealer.models import DealerOrders, DealertLocation, DealerUsers
from NapsackAdmin.models import Products as NapProducts
from . import locationfunctions
import datetime
#
# def updatecart(data):

def finddealer(lat, long):
    dlr_loc = DealertLocation.objects.filter(dealer_status=True).values()
    find_dis = 0
    find_dlr = [0, 1]
    for dlr_one in dlr_loc:
        dis = locationfunctions.find_distance(lat,long,dlr_one['latitude'],dlr_one['longitude'])
        if dis >= find_dis:
            dlr_orders = DealerOrders.objects.filter(dealer_status=False).values()
            if len(dlr_orders) <=5:
                find_dis = dis
                find_dlr[0] = dlr_one
                find_dlr[1] = dis
    if find_dis == 0:
        dlr_one = dlr_loc[0]
        find_dlr[0] = dlr_one
        find_dlr[1] = dis
    return find_dlr


def FindEachDistamce(distance):
    time = 0
    if distance <= 5:
        time = distance * 2
    elif distance <= 10 and distance > 5:
        time = distance * 2 + 5
    elif distance <= 15 and distance > 10:
        time = distance * 2 + 10
    elif distance <= 20 and distance > 15:
        time = distance * 2 + 15
    elif distance <= 25 and distance > 20:
        time = distance * 2 + 20
    return time

def FindDeliveryDateAndTime(a_distance, c_distance):
    a_time = FindEachDistamce(a_distance)
    d_time = FindEachDistamce(c_distance)
    total_time = a_time + d_time
    current_time = datetime.datetime.now()
    h = current_time.hour
    m = current_time.minute
    s = current_time.second
    if total_time + m >=60 and total_time + m < 120:
        h = h + 1
        m = m + total_time - 60
    elif total_time + m >= 120 and total_time + m < 180:
        h = h + 2
        m = m + total_time - 120
    elif total_time + m >= 180 and total_time + m < 240:
        h = h + 3
        m = m + total_time - 180
    elif total_time + m >= 240 and total_time + m < 300:
        h = h + 4
        m = m + total_time - 240
    elif total_time + m >= 300 and total_time + m < 360:
        h = h + 5
        m = m + total_time - 300
    if h > 23:
        h = h - 24
    d = datetime.datetime(current_time.year, current_time.month, current_time.day, h, int(m), s, current_time.microsecond)
    
    return d


def updateorders(data,user_id,shop_id, lat, long):
    us = models.CustomerUsers.objects.get(user_id=user_id)
    # corder =  models.CustomerOrders(customerusername=us, bill=amt, status= "Order Placed", payment_id= payment_id)
    # shop_id = '0210204445e14f4395a6042a914641e9'
    Auid = AgentShopCategorie.objects.filter(agent_shop_categorie_id=shop_id).values()
    uid_one = Auid[0]
    Aun_get = AgentsUsers.objects.get(agen_user_id=uid_one['username_id'])
    l = len(data)
    # t_uuid = uuid.uuid4()
    aorder = AgentOrders(agent_order_id=payments.customer_order_id,agentsusers=Aun_get,bill=data[l-1],delivery_info="Order Not Send")
    aorder.save()
    # corder.save()
    corder_get = models.CustomerOrders.objects.get(order_id=payments.customer_order_id)
    aorder_get = AgentOrders.objects.get(agent_order_id=payments.customer_order_id)
    dlr = finddealer(lat,long)
    d = dlr[0]
    c_to_d_dis = dlr[1]
    dlr_one = d['username_id']
    dlr_get = DealerUsers.objects.get(dealer_user_id=dlr_one)
    dlr_order_id = uuid.uuid4()
    dlr_order = DealerOrders(order_id=payments.customer_order_id, status="Order Not Deliver",
                             username = dlr_get, agent_order_id = aorder_get, customer_order_id = corder_get)
    dlr_order.save()
    # member.firstname = "first"
    # member.lastname = "last"
    # member.save()
    for i in range(0, len(data)-1):
        pro = data[i]
        corderproduct = models.CustomerProducts(
            name=pro['product_name'],Categorie=pro['Categories_name'],
            cost= pro['cost'], quantity=pro['qty_selected'], customerorders=corder_get)
        corderproduct.save()
        aorderproduct = AgentOrdersProducts(
            agentorders= aorder_get,name=pro['product_name'],
            Categorie=pro['Categories_name'],cost=pro['cost'],quantity=pro['qty_selected']
        )
        aorderproduct.save()
    models.CustomerCart.objects.filter(customerusername=us).delete()





def UpdateCOD(user_id,lat, long,data,shop_id):
    te_uuid = uuid.uuid4()
    l = len(data)
    dlr = finddealer(lat, long)
    d = dlr[0]
    c_to_d_dis = dlr[1]
    auser_lat_log = AgentLocation.objects.filter(username_id=shop_id).values()
    auser_lat_log_one = auser_lat_log[0]
    find_dis_a = locationfunctions.find_distance(d['latitude'], d['longitude'], auser_lat_log_one['latitude'], auser_lat_log_one['longitude'])
    deliver_time = FindDeliveryDateAndTime(find_dis_a, c_to_d_dis)
    un = models.CustomerUsers.objects.get(user_id=user_id)
    cus_pay_update = models.CustomerOrders(order_id=te_uuid,
                                           payment_id="Cash and Delivery",status="Order Placed",bill=data[l - 1],
                                           customerusername=un, longitude= long,latitude=lat, payment_mode="Pay on Delivery", delivery_date=deliver_time)
    cus_pay_update.save()
    # Auid = AgentShopCategorie.objects.filter(agent_shop_categorie_id=shop_id).values()
    # uid_one = Auid[0]
    Aun_get = AgentsUsers.objects.get(agen_user_id=shop_id)
    # t_uuid = uuid.uuid4()
    aorder = AgentOrders(agent_order_id=te_uuid, agentsusers=Aun_get, bill=data[l - 1],
                         delivery_info="Order Not Send", delivery_date=deliver_time)
    aorder.save()
    # corder.save()
    corder_get = models.CustomerOrders.objects.get(order_id=te_uuid)
    aorder_get = AgentOrders.objects.get(agent_order_id=te_uuid)
    dlr_one = d['username_id']
    dlr_get = DealerUsers.objects.get(dealer_user_id=dlr_one)
    dlr_order = DealerOrders(order_id=te_uuid, status="Order Not Deliver",
                             username=dlr_get, agent_order_id=aorder_get, customer_order_id=corder_get, delivery_date=deliver_time)
    dlr_order.save()
    print(len(data))
    for i in range(0, len(data) - 1):
        pro = data[i]
        pro_id = pro['nap_product_id']
        nap_pro = NapProducts.objects.filter(product_id=pro_id).values()
        nap_one = nap_pro[0]
        img_url = nap_one['image']
        corderproduct = models.CustomerProducts(
            name=pro['product_name'], Categorie=pro['Categories_name'],
            cost=pro['cost'], quantity=pro['qty_selected'], customerorders=corder_get, image=img_url)
        corderproduct.save()
        aorderproduct = AgentOrdersProducts(
            agentorders=aorder_get, name=pro['product_name'],
            Categorie=pro['Categories_name'], cost=pro['cost'], quantity=pro['qty_selected'], image=img_url
        )
        aorderproduct.save()
        a_get_qty = AgentProducts.objects.filter(agentsusers_id=shop_id,product_id=pro_id).values()
        a_get_qty_one = a_get_qty[0]
        AgentProducts.objects.filter(product_id=pro_id, agentsusers_id=shop_id).update(quantity_present=a_get_qty_one['quantity_present']-int(pro['qty_selected']))
    models.CustomerCart.objects.filter(customerusername=un).delete()   