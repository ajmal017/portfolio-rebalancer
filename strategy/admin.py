from django.contrib import admin
from .models import Strategy
# Register your models here.
class StrategyAdmin(admin.ModelAdmin):
	list_display = ('name', 'source', 'funds', 'created')




admin.site.register(Strategy, StrategyAdmin)