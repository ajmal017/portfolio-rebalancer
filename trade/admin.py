from django.contrib import admin
from .models import Trade
# Register your models here.
class TradeAdmin(admin.ModelAdmin):
	def strategy(self, obj):
		return str(obj.strategy.name)

	def trading_account(self, obj):
		return str(obj.trading_account.platform_name)

	list_display = ('strategy', 'trade_fund', 'trading_account', 'timestamp')

	



admin.site.register(Trade, TradeAdmin)