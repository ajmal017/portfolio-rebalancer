from django.contrib import admin
from .models import Target, VAAStrategy, VTSEmail
from django.db.models import Q
# Register your models here.
class TargetAdmin(admin.ModelAdmin):
	list_display = ('strategy', 'ticker', 'target',  'date')

	def get_queryset(self, request):
		qs = super(TargetAdmin, self).get_queryset(request)
		return qs.exclude(Q(strategy='VAA Strategy') Q(strategy="VTSEmail"))



admin.site.register(Target, TargetAdmin)





class VAAStrategyAdmin(admin.ModelAdmin):
	list_display = ('strategy', 'ticker', 'get_target', 'date')

	def get_target(self, obj):
		return str(obj.target) + '%'
	def get_queryset(self, request):
		qs = super(VAAStrategyAdmin, self).get_queryset(request)
		return Target.objects.filter(strategy='VAA Strategy')
		



admin.site.register(VAAStrategy, VAAStrategyAdmin)



class VTSEmailAdmin(admin.ModelAdmin):
	list_display = ('strategy', 'ticker', 'target', 'date')
	def has_add_permission(self, request, obj=None):
		return False
	def get_queryset(self, request):
		qs = super(VTSEmailAdmin, self).get_queryset(request)
		return Target.objects.filter(strategy='VAA Str')


admin.site.register(VTSEmail, VTSEmailAdmin)