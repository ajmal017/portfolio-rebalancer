from django.contrib import admin
from .models import Strategy
# Register your models here.
class StrategyAdmin(admin.ModelAdmin):
	
	list_display = ('name', 'scrape_frequency', 'display_name', 'source', 'get_funds', 'is_active')
	def get_funds(self, obj):
		return '$ ' + str(obj.funds)
	get_funds.short_description = 'Allocated Funds'



admin.site.register(Strategy, StrategyAdmin)