from django.contrib import admin
from .models import Strategy
# Register your models here.
class StrategyAdmin(admin.ModelAdmin):
	list_display = ('name', 'source', 'get_funds', 'created')
	def get_funds(self, obj):
		return str(obj.funds) + '$'



admin.site.register(Strategy, StrategyAdmin)