from django.contrib import admin

from transaction.models import FlexAccount, Transaction


admin.site.register(FlexAccount)
admin.site.register(Transaction)

# Register your models here.
