from django.db import models
from scraping_events.models import Target
# Create your models here.

class IBTicker(models.Model):
	class Meta:
		verbose_name = "IB Tikcker"
		verbose_name_plural = "IB Tickers"
	ticker = models.OneToOneField(Target, on_delete=models.CASCADE, blank=False, null=True)
	con_id = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "{}-{}".format(self.ticker, self.con_id)
