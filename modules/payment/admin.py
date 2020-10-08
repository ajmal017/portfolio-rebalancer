from django.contrib import admin
from .models import PaymentHistory, PaymentDue
from django.db.models import Q
# Register your models here.
class PaymentHistoryAdmin(admin.ModelAdmin):
	list_display=['booking', 'transaction_id', 'amount', 'created_at']
	fields = ('booking', 'status', 'transaction_id', 'amount')
	def has_add_permission(self, obj):
		return False
	def has_change_permission(self, request, obj=None):
		return False

class PaymentDueAdmin(admin.ModelAdmin):
	list_display=['booking', 'transaction_id', 'amount', 'created_at']
	fields = ('booking', 'status', 'transaction_id', 'amount')
	def has_add_permission(self, obj):
		return False
	def has_change_permission(self, request, obj=None):
		return True
	def get_queryset(self, request):
		qs = super(PaymentDueAdmin, self).get_queryset(request)
		return qs.filter(Q(status="") | Q(status="Failed"))

admin.site.register(PaymentDue, PaymentDueAdmin)

admin.site.register(PaymentHistory, PaymentHistoryAdmin)