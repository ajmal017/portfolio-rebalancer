from django.contrib import admin
from .models import Target, VAAStrategy, VTSEmail
from strategy.models import Strategy
from django.db.models import Q
from django.db.models import Count
import pdb
# from .forms import *

from django.utils.safestring import mark_safe

# Register your models here.
class TargetAdmin(admin.ModelAdmin):
    # form = MyModelForm
    list_display = ('strategy', 'ticker','target', 'is_tradeable', 'date')
    # change_list_template = 'admin/sale_summary_change_list.html'
    def has_delete_permission(self, request, obj=None):
        return False
    def get_queryset(self, request):
        qs = super(TargetAdmin, self).get_queryset(request)
        return qs.exclude(Q(strategy='VAA Strategy')| Q(strategy="VTSEmail"))
    def has_add_permission(self, request, obj=None):
        return False
    fieldsets = (
        ("", {
        'classes': ('wide',),
        'fields': ('account_number','strategy', 'ticker', 'target','is_tradeable', 'date',)}
        ),
        # ('Account', {'fields': ('Info','pay_now',) })
    )

    def account_number(self, obj):
        # Strategy.objects.filter()
        try:
        	pdb.set_trace()
            strategy = Strategy.objects.filter(display_name=obj.strategy)
            if strategy.exists():

                return strategy.first().account_number.trading_account.account_number
            return ''
        except Exception as ex:
            print(str(ex))
            return ''
        # try:
        # 	return obj.strategy_id.account_number
        # except:
        # 	return ""




    # def get_readonly_fields(self, request, obj=None):
    #     if obj: # editing an existing object

    #         return self.readonly_fields + ('field1', 'field2')
    #     return self.readonly_fields

    # def get_object(self, request, object_id, mno):
    #     obj = super(TargetAdmin, self).get_object(request, object_id)
    #     # for key, value in request.GET.items():
    #         # print(key, value)
    #         # strategy_id_id
    #     setattr(obj, 'strategy_id_id', '52')
    #     return obj

    def has_change_permission(self, request, obj=None):
        return False

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
    
    list_display = ('strategy', 'ticker', 'get_target', 'is_tradeable', 'date')
    def get_target(self, obj):
        return str(obj.target) + '%'
    get_target.short_description = 'Target'
    def get_queryset(self, request):
        qs = super(VAAStrategyAdmin, self).get_queryset(request)
        return Target.objects.filter(strategy='VAA Strategy').exclude(target='0')
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    fieldsets = (
        ("", {
        'classes': ('wide',),
        'fields': ('account_number','strategy', 'ticker', 'target','is_tradeable', 'date',)}
        ),
        # ('Account', {'fields': ('Info','pay_now',) })
    )
    def account_number(self, obj):
        # Strategy.objects.filter()
        try:
            strategy = Strategy.objects.filter(display_name=obj.strategy)
            if strategy.exists():

                return strategy.first().account_number.trading_account.account_number
            return ''
        except Exception as ex:
            print(str(ex))
            return ''
        # try:
        # 	return obj.strategy_id.account_number
        # except:
        # 	return ""
    def has_change_permission(self, request, obj=None):
        return False
		



admin.site.register(VAAStrategy, VAAStrategyAdmin)



class VTSEmailAdmin(admin.ModelAdmin):
    list_display = ('strategy', 'ticker', 'get_target', 'is_tradeable', 'date')
    def get_target(self, obj):
        return str(obj.target) + '%'
    get_target.short_description = 'Target'
    def has_add_permission(self, request, obj=None):
        return False
    def get_queryset(self, request):
        qs = super(VTSEmailAdmin, self).get_queryset(request)
        return Target.objects.filter(strategy='VTSEmail')

    fieldsets = (
        ("", {
        'classes': ('wide',),
        'fields': ('account_number','strategy', 'ticker', 'target','is_tradeable', 'date',)}
        ),
        # ('Account', {'fields': ('Info','pay_now',) })
    )
    def account_number(self, obj):
        # Strategy.objects.filter()
        try:
            strategy = Strategy.objects.filter(display_name=obj.strategy)
            if strategy.exists():

                return strategy.first().account_number.trading_account.account_number
            return ''
        except Exception as ex:
            print(str(ex))
            return ''
        # try:
        # 	return obj.strategy_id.account_number
        # except:
        # 	return ""
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(VTSEmail, VTSEmailAdmin)