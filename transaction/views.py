
import requests
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import *
from accounts.serializer import *
from .serializers import *
from django.http import HttpResponse, JsonResponse


@permission_classes((IsAuthenticated, ))
@method_decorator(csrf_exempt)
def get_account_name(request):
    if requests.method == 'POST':

        phone = request.POST.get('phone')

        receiver_account_name = User.objects.filter(phone=phone)
        serializer = UserSerializer(receiver_account_name, many=True)
        if serializer.data == []:
            return JsonResponse({'error': 'user with phone number does not exist'})
        else:
            return JsonResponse(serializer.data[0], safe=False)


@permission_classes((IsAuthenticated, ))
@method_decorator(csrf_exempt)
def transfer_money(request):
    phone = request.POST.get('account')
    amount = request.POST.get('amount')
    sender_account = FlexAccount.objects.get(account_owner=request.user)
    receiver_email = User.objects.get(phone=phone)
    receiver_account = FlexAccount.objects.get(account_owner=receiver_email)
    print(sender_account.balance)

    if(sender_account.balance < float(amount)):
        return JsonResponse({'error': 'account balance is not enough'})
    else:
        sender_account.balance = float(
            sender_account.balance) - float(float(amount))
        receiver_account.balance = float(
            receiver_account.balance) + float(float(amount))
        sender_account.save()
        receiver_account.save()
        print(sender_account.balance)
        print(receiver_account.balance)
        return JsonResponse({'sucess': 'Transaction sucessfull'})


@method_decorator(csrf_exempt)
def deposit_fund(request):
    email = request.POST.get('email')
    amount = request.POST.get('amount')
    data = {
        'email': email,
        'amount': amount
    }
    url = 'https://api.paystack.co/transaction/initialize'
    headers = {
        "authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    r = requests.post(url, headers=headers, data=data)
    response = r.json()
    print(response)
    Transaction.objects.create(
        account=FlexAccount.objects.get(account_owner=email),
        transaction_type="deposit",
        amount=data["amount"],
        # paystack_payment_reference=response['data']['reference'],
        paystack_payment_reference='fhshbdshsj',
        status="pending",
    )
    return JsonResponse(response)
