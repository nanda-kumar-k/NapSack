from instamojo_wrapper import Instamojo

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


def UpdatePayments(payment_id,payment_request_id,payment_status,user_id,lat, long):
    amt = Amount_paid(payment_id,payment_request_id)
    # user_id = 'cf4b8ec9ff1844c980360339379a7313'
    nap_pay_upadte = AllPayments(
        payment_id=payment_id, payment_request_id=payment_request_id,
        payment_status=payment_status,user_id=user_id,amount_paid=amt)
    nap_pay_upadte.save()
    te_uuid = uuid.uuid4()
    global customer_order_id
    customer_order_id = te_uuid
    un = models.CustomerUsers.objects.get(user_id=user_id)
    cus_pay_update = models.CustomerOrders(order_id=te_uuid,
                                           payment_id=payment_id,status=payment_status,bill=amt,
                                           customerusername=un, longitude= long,latitude=lat, payment_mode="Online Payment")
    cus_pay_update.save()