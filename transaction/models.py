from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class FlexAccount(models.Model):
    account_owner = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True)

    balance = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return self.account_owner.__str__()


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'deposit'),
        ('transfer', 'transfer'),
        ('withdraw', 'withdraw'),
    )
    account = models.ForeignKey(
        FlexAccount, on_delete=models.CharField, null=True)
    transaction_type = models.CharField(
        max_length=200, null=True,  choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=100, null=True, decimal_places=2)
    status = models.CharField(max_length=100, default="pending")
    paystack_payment_reference = models.CharField(
        max_length=100, default='', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account.__str__()

    # def __int__(self):
    #     return self.amount
