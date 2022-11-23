
import requests
from django.conf import settings
from django.db.models import Sum
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlexAccount
        fields = '__all__'


class FlexAccountSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()

    def get_balance(self, obj):
        bal = Transaction.objects.filter(
            wallet=obj, status="success").aggregate(Sum('amount'))['amount__sum']
        return bal


def is_amount(value):
    if value <= 0:
        raise serializers.ValidationError({"detail": "Invalid Amount"})
    return value


class DepositSerializer(serializers.Serializer):

    amount = serializers.IntegerField(validators=[is_amount])
    email = serializers.EmailField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            return value
        raise serializers.ValidationError({"detail": "Email not found"})

    def save(self):
        user = self.context['request'].user
        account = FlexAccount.objects.get(user=user)
        data = self.validated_data
        url = 'https://api.paystack.co/transaction/initialize'
        headers = {"authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        r = requests.post(url, headers=headers, data=data)
        response = r.json()
        print(response)
        # Transaction.objects.create(
        #     account=account,
        #     transaction_type="deposit",
        #     amount=data["amount"],
        #     paystack_payment_reference=response['data']['reference'],
        #     status="pending",
        # )
