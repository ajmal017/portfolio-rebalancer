from django.contrib import admin
from .models import Strategy
# Register your models here.
class StrategyAdmin(admin.ModelAdmin):
	def funds(self, obj):
		return '$ ' + str(obj.funds)
	list_display = ('name', 'scrape_frequency', 'is_active', 'display_name', 'source', 'funds', 'created')
	



admin.site.register(Strategy, StrategyAdmin)