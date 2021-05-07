from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Strategy(models.Model):
	
	class Meta:
		verbose_name = "Strategy"
		verbose_name_plural = "Strategies"

	PORTFOLIO_VISUALIZER = 'PORTFOLIO VISUALIZER'
	VTS_EMAIL = 'VTS EMAIL'
	VAA_STRATEGY = 'VAA STRATEGY'
	

	TYPES = (
		(PORTFOLIO_VISUALIZER, ('Portfolio Visualizer')), 
		(VTS_EMAIL, ('VTS Email')), 
		(VAA_STRATEGY, ('VAA Strategy'))
	)
	SCRAPEFREQUENCY = (
        ('Daily','Daily'),
        ('Weekly','Weekly'),
        ('Monthly','Monthly')
    )
	name = models.CharField(verbose_name="Strategy Name", max_length=300)
	# source = models.CharField(verbose_name="Data Source", max_length=300)
	scrape_frequency = models.CharField(verbose_name=('Scrape Frequency'), max_length=50, default='Daily', choices=SCRAPEFREQUENCY)
	is_active = models.BooleanField(default=False)
	display_name = models.CharField(verbose_name="Display Name", max_length=200, blank=False, null=True)
	source =  models.CharField(verbose_name=('Data Source'), max_length=100, blank=False, choices=TYPES, null=True)
	funds = models.CharField(verbose_name="Allocated Funds", max_length=300)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	def clean(self, *args, **kwargs):
		name = str(self.name)
		if name and Strategy.objects.filter(name=name).exclude(id=self.id):
			raise ValidationError('Strategy name already exists')
		super(Strategy, self).clean(*args, **kwargs)
