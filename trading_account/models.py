from django.db import models

# Create your models here.
class TradingAccount(models.Model):
	class Meta:
		verbose_name = "Trading Accounts"
		verbose_name_plural = "Trading Accounts"

	# (ENUM 'E-Trade','IB','Fidelity') Default 'E-Trade'
	E_TRADE = 'E-Trade'
	IB = 'IB'
	FIDELITY = 'Fidelity'
	
	TYPES = (
		(E_TRADE, ('E-Trade')), 
		(IB, ('IB')), 
		(FIDELITY, ('Fidelity'))
	)
	platform_name = models.CharField(verbose_name=('Platform Name'), max_length=100, blank=True, choices=TYPES, null=False, default="E_TRADE")
	account_name = models.CharField(verbose_name="Account Name",  max_length=100, blank=False, null=False)
	account_number = models.CharField(verbose_name="Account Number", max_length=100, blank=False, null=False)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.platform_name


