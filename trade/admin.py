from django.contrib import admin
from .models import Trade
# Register your models here.
class TradeAdmin(admin.ModelAdmin):
    def strategy(self, obj):
        return str(obj.strategy_id.name)

    def trading_account(self, obj):
        return str(obj.trading_account.platform_name)
    def has_delete_permission(self, request, obj=None):
        return False
    list_display = ('strategy_id', 'trading_account', 'timestamp')

    fieldsets = (
        ("", {
        'classes': ('wide',),
        'fields': ('strategy_id', 'trading_account', 'positions','timestamp')}
        ),
        # ('Account', {'fields': ('Info','pay_now',) })
    )

    def strategy_id(self, obj):
        # Strategy.objects.filter()
        try:
            # strategy = Strategy.objects.filter(display_name=obj.strategy)
            # if strategy.exists():

            #     return strategy.first().account_number.trading_account.account_number
            # return ''
            return obj.strategy_id.name
        except Exception as ex:
            print(str(ex))
            return ''
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

	



admin.site.register(Trade, TradeAdmin)