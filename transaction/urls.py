
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('t', transfer_money),
    path('g/', get_account_name),
    path('deposit/', deposit_fund)
]
