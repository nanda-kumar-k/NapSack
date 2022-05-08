from . import models
from Agents.models import AgentOrders, AgentOrdersProducts, AgentShopCategorie, AgentsUsers
from . import payments
import uuid
from Dealer.models import DealerOrders, DealertLocation, DealerUsers
from . import locationfunctions
#
# def updatecart(data):

def finddealer(lat, long):
    dlr_loc = DealertLocation.objects.filter(dealer_status=True).values()
    find_dis = 0
    find_dlr = [0]
    for dlr_one in dlr_loc:
        dis = locationfunctions.find_distance(lat,long,dlr_one['latitude'],dlr_one['longitude'])
        if dis >= find_dis:
            dlr_orders = DealerOrders.objects.filter(dealer_status=False).values()
            if len(dlr_orders) <=5:
                find_dis = dis
                find_dlr[0] = dlr_one
    if find_dis == 0:
        dlr_one = dlr_loc[0]
        find_dlr[0] = dlr_one
    return find_dlr


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
    dlr_one = d['username_id']
    print("ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
    print(dlr_one)
    dlr_get = DealerUsers.objects.get(dealer_user_id=dlr_one)
    dlr_order_id = uuid.uuid4()
    dlr_order = DealerOrders(order_id=payments.customer_order_id, status="Order Not Deliver",
                             username = dlr_get, agent_order_id = aorder_get, customer_order_id = corder_get)
    dlr_order.save()
    # member.firstname = "first"
    # member.lastname = "last"
    # member.save()
    print("tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt")
    print(len(data))

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
    un = models.CustomerUsers.objects.get(user_id=user_id)
    cus_pay_update = models.CustomerOrders(order_id=te_uuid,
                                           payment_id="Cash and Delivery",status="Cash and Delivery",bill=data[l - 1],
                                           customerusername=un, longitude= long,latitude=lat, payment_mode="Online Payment")
    cus_pay_update.save()
    # Auid = AgentShopCategorie.objects.filter(agent_shop_categorie_id=shop_id).values()
    # uid_one = Auid[0]
    Aun_get = AgentsUsers.objects.get(agen_user_id=shop_id)
    # t_uuid = uuid.uuid4()
    aorder = AgentOrders(agent_order_id=te_uuid, agentsusers=Aun_get, bill=data[l - 1],
                         delivery_info="Order Not Send")
    aorder.save()
    # corder.save()
    corder_get = models.CustomerOrders.objects.get(order_id=te_uuid)
    aorder_get = AgentOrders.objects.get(agent_order_id=te_uuid)
    dlr = finddealer(lat, long)
    d = dlr[0]
    dlr_one = d['username_id']
    print("ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
    print(dlr_one)
    dlr_get = DealerUsers.objects.get(dealer_user_id=dlr_one)
    dlr_order = DealerOrders(order_id=te_uuid, status="Order Not Deliver",
                             username=dlr_get, agent_order_id=aorder_get, customer_order_id=corder_get)
    dlr_order.save()
    print(len(data))
    for i in range(0, len(data) - 1):
        pro = data[i]
        corderproduct = models.CustomerProducts(
            name=pro['product_name'], Categorie=pro['Categories_name'],
            cost=pro['cost'], quantity=pro['qty_selected'], customerorders=corder_get)
        corderproduct.save()
        aorderproduct = AgentOrdersProducts(
            agentorders=aorder_get, name=pro['product_name'],
            Categorie=pro['Categories_name'], cost=pro['cost'], quantity=pro['qty_selected']
        )
        aorderproduct.save()
    models.CustomerCart.objects.filter(customerusername=un).delete()
