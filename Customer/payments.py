from instamojo_wrapper import Instamojo
from Agents.models import AgentLocation, AgentOrders, AgentOrdersProducts, AgentsUsers
from Customer import locationfunctions
from NapsackAdmin.models import Products as NapProducts
from Customer.cartfunctions import FindDeliveryDateAndTime, finddealer
from Dealer.models import DealerOrders, DealerUsers

from . import models

from NapsackAdmin.models import AllPayments
import uuid

API_KEY = ''
AUTH_TOKEN = ''
api = Instamojo(api_key='2730e85d125f7bd19d114690cce9be5c',
                    auth_token='8c74c74003ddda5ca4f6d787ac06fa9c')

payment_request_id_verify= "b5ede769cd624012b084c04f004a89f9"

customer_order_id = ""

def get_payment_url(amount, currentuser):
    # userinfo = models.CustomerUsers.objects.filter(user_id=currentuser).values()
    # data = userinfo[0]
    # response = api.payment_request_create(
    #     buyer_name=data['username'],
    #     phone=data['phone_number'],
    #     email=data['email'],
    #     purpose='NapSack Order Payment',
    #     amount=9,
    #     send_email=True,
    #     send_sms=True,
    #     allow_repeated_payments=False,
    #     redirect_url="http://127.0.0.1:8000/customer/payment/"
    # )
    # # print(response)
    # url = response['payment_request']['longurl']
    # payment_request_id = response['payment_request']['id']
    # pay_url_id = 'https://www.instamojo.com/@napsack/669dcfe55a2e496fb88f34f300fdb545'
    # global payment_request_id_verify
    # payment_request_id_verify = payment_request_id
    # pay_url_id = url
    pay_url_id = "http://127.0.0.1:8000/payment/?payment_id=MOJO2426W05Q20487814&payment_status=Credit&payment_request_id=b5ede769cd624012b084c04f004a89f9"
    return pay_url_id


def verify_payment(payment_id,payment_request_id):
    response = api.payment_request_payment_status(payment_request_id, payment_id)
    status = response['payment_request']['payment']['status']
    print("tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt")
    print(status)
    if status == "Credit" and payment_request_id_verify == payment_request_id:
        print("True")
        return True
    else:
        return False


def Amount_paid(payment_id,payment_request_id):
    response = api.payment_request_payment_status(payment_request_id, payment_id)
    amount = response['payment_request']['payment']['amount']
    return amount


def UpdatePayments(payment_id,payment_request_id,payment_status,user_id,lat, long,data,shop_id):
    amt = Amount_paid(payment_id,payment_request_id)
    nap_pay_upadte = AllPayments(
        payment_id=payment_id, payment_request_id=payment_request_id,
        payment_status=payment_status,user_id=user_id,amount_paid=amt)
    nap_pay_upadte.save()
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
                                           payment_id=payment_id,status="Order Placed",bill=amt,
                                           customerusername=un, longitude= long,latitude=lat, payment_mode=payment_status, delivery_date=deliver_time)
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
            Categorie=pro['Categories_name'], cost=pro['cost'], quantity=pro['qty_selected']
        )
        aorderproduct.save()
    models.CustomerCart.objects.filter(customerusername=un).delete()