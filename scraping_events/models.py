from django.db import models
from strategy.models import Strategy
# Create your models here.
# class Targets(Base):
#     __tablename__ = 'targets'

#     id = Column(Integer, primary_key=True)
#     ticker = Column(String(100))
#     target = Column(String(100))
#     strategy = Column(String(100))
#     date = Column(Date)




# TODO: Remove delete and edit power

class Target(models.Model):
	class Meta:
		verbose_name = "Portfolio Visualizer"
		verbose_name_plural = "Portfolio Visualizer"

	strategy_id = models.ForeignKey(Strategy, blank=True, null=True, on_delete=models.CASCADE)

	ticker = models.CharField(max_length=200)
	target = models.CharField(max_length=200) # TODO: percentage_allocation
	strategy = models.CharField(max_length=200) # TODO: Dropdown from Strategies table as FK
	# con_id = models.CharField(max_length=100, blank=True)
	# last_fetched_price = models.CharField(max_length=100, blank=True, null=True)
	# current_position = models.CharField(max_length=100, blank=True, null=True)
	# updated_position = models.CharField(max_length=100, blank=True, null=True)
	is_tradeable = models.BooleanField(default=False)
	date = models.DateTimeField()
	created = models.DateTimeField(auto_now_add=True)

	
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