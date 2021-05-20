from django.db import models
from trading_account.models import TradingAccount
# from strategy.models import Strategy

# Create your models here.
class Trade(models.Model):
	
	class Meta:
		verbose_name = "Completed Trades"
		verbose_name_plural = "Completed Trades"
	# TOD): rename strategy to strategy_id
	strategy_id = models.ForeignKey(to="strategy.Strategy", blank=False, null=False, on_delete=models.CASCADE)

	# trade_fund = models.IntegerField(verbose_name="Total Trade fund")
	trading_account = models.ForeignKey(TradingAccount, blank=False, null=False, on_delete=models.CASCADE)
	positions = models.IntegerField(blank=True, null=False)
	timestamp = models.DateTimeField(auto_now_add=True)
	# TODO: Add positions


	def __str__(self):
		return self.trading_account.account_number