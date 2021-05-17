from django.db import models

# Create your models here.
# class Targets(Base):
#     __tablename__ = 'targets'

#     id = Column(Integer, primary_key=True)
#     ticker = Column(String(100))
#     target = Column(String(100))
#     strategy = Column(String(100))
#     date = Column(Date)


class Target(models.Model):
	class Meta:
		verbose_name = "Portfolio Visualizer"
		verbose_name_plural = "Portfolio Visualizer"

	ticker = models.CharField(max_length=200)
	target = models.CharField(max_length=200)
	strategy = models.CharField(max_length=200)
	# con_id = models.CharField(max_length=100, blank=True)
	last_fetched_price = models.CharField(max_length=100, blank=True, null=True)
	is_tradeable = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.ticker


class VAAStrategy(Target):
	class Meta:
		verbose_name = "VAA Strategy"
		verbose_name_plural = "VAA Strategy"
		proxy = True

class VTSEmail(Target):
	class Meta:
		verbose_name = "VTS Email"
		verbose_name_plural = "VTS Email"
		proxy = True

class Employee(models.Model):
        ename = models.CharField(max_length=100)