from django.contrib import admin
from .models import Strategy
# Register your models here.
class StrategyAdmin(admin.ModelAdmin):
	def funds(self, obj):
		return '$ ' + str(obj.funds)
	list_display = ('name', 'scrape_frequency', 'display_name', 'source', 'funds', 'is_active','created')
	



admin.site.register(Strategy, StrategyAdmin)