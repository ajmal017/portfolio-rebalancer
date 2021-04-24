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
	ticker = models.CharField(max_length=200)
	target = models.CharField(max_length=200)
	strategy = models.CharField(max_length=200)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.ticker