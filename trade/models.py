from django.db import models
from trading_account.models import TradingAccount
from strategy.models import Strategy
# Create your models here.
class Trade(models.Model):
	
	class Meta:
		verbose_name = "Completed Trades"
		verbose_name_plural = "Completed Trades"
	
	strategy = models.ForeignKey(Strategy, blank=False, null=False, on_delete=models.CASCADE)
	trade_fund = models.IntegerField(verbose_name="Total Trade fund")
	trading_account = models.ForeignKey(TradingAccount, blank=False, null=False, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)