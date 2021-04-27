from django.db import models

# Create your models here.
class Strategy(models.Model):
	
	class Meta:
		verbose_name = "Strategy"
		verbose_name_plural = "Strategies"
	
	name = models.CharField(verbose_name="Strategy Name", max_length=300)
	source = models.CharField(verbose_name="Data Source", max_length=300)
	funds = models.CharField(verbose_name="Allocated Funds", max_length=300)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name
