from django.contrib import admin
from .models import Target, VAAStrategy, VTSEmail
from django.db.models import Q
from django.db.models import Count
# Register your models here.
class TargetAdmin(admin.ModelAdmin):
    list_display = ('strategy', 'ticker','target', 'last_fetched_price', 'is_tradeable','date')
    # change_list_template = 'admin/sale_summary_change_list.html'
    def get_queryset(self, request):
        qs = super(TargetAdmin, self).get_queryset(request)
        return qs.exclude(Q(strategy='VAA Strategy')| Q(strategy="VTSEmail"))

    # def changelist_view(self, request, extra_context=None):
    #     response = super().changelist_view(
    #         request,
    #         extra_context=extra_context,
    #     )
    #     try:
    #         qs = response.context_data['cl'].queryset
    #     except (AttributeError, KeyError):
    #         return response
        
    #     metrics = {
    #         'total': Count('id')
    #         # ‘total_sales’: Sum(‘price’),
    #     }
    #     response.context_data['custom_targets'] = list(
    #         qs
    #         .values('strategy')
    #         .annotate(**metrics)
    #         .order_by()
    #     )
    #     # [{'strategy': 'Adaptive-C', 'total': 2}, {'strategy': 'Adaptive-D', 'total': 2},
    #     #  {'strategy': 'Adaptive-E', 'total': 1}, {'strategy': 'MovingAvg-A', 'total': 1}, {'strategy': 'MovingAvg-B', 'total': 2}]
    #     for q in response.context_data['custom_targets']:
    #     	tickers = qs.filter(strategy=q.get('strategy')).values_list('ticker', flat=True)
    #     	tickers = qs.filter(strategy=q.get('strategy')).values_list('ticker', flat=True)
    #     	tickers_to_str = ", ".join(tickers)
    #     	q.update({'tickers': tickers_to_str})
    #     return response


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
		return Target.objects.filter(strategy='VTSEmail')


admin.site.register(VTSEmail, VTSEmailAdmin)