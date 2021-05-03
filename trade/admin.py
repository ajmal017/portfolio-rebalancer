from django.contrib import admin
from .models import Trade
# Register your models here.
class TradeAdmin(admin.ModelAdmin):
	list_display = ('get_strategy', 'trade_fund', 'get_trading_account', 'timestamp')

	def get_strategy(self, obj):
		return str(obj.strategy.name)

	def get_trading_account(self, obj):
		return str(obj.trading_account.platform_name)



admin.site.register(Trade, TradeAdmin)