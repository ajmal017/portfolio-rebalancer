from django.db import models
from scraping_events.models import Target
# Create your models here.

class IBTicker(models.Model):
	class Meta:
		verbose_name = "IB Tikcker"
		verbose_name_plural = "IB Tickers"
	ticker = models.CharField(max_length=100)
	con_id = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "{}-{}".format(self.ticker, self.con_id)
