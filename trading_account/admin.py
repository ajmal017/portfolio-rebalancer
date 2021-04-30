from django.contrib import admin
from .models import TradingAccount
# Register your models here.
class TradingAccountAdmin(admin.ModelAdmin):
	list_display = ('platform_name', 'account_name', 'account_number', 'created')



admin.site.register(TradingAccount, TradingAccountAdmin)