from django.db import models

# Create your models here.
class Strategy(models.Model):
	
	class Meta:
		verbose_name = "Strategy"
		verbose_name_plural = "Strategies"

	PORTFOLIO_VISUALIZER = 'PORTFOLIO VISUALIZER'
	VTS = 'VTS'
	TRENDXPLRER = 'TRENDXPLRER'
	

	TYPES = (
		(PORTFOLIO_VISUALIZER, ('Portfolio Visualizer')), 
		(VTS, ('VTS')), 
		(TRENDXPLRER, ('TrendXpLrer'))
	)
	name = models.CharField(verbose_name="Strategy Name", max_length=300)
	# source = models.CharField(verbose_name="Data Source", max_length=300)
	source =  models.CharField(verbose_name=('Data Source'), max_length=100, blank=False, choices=TYPES, null=True)
	funds = models.CharField(verbose_name="Allocated Funds", max_length=300)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name
