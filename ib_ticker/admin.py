from django.contrib import admin
from .models import IBTicker
from django.utils.html import format_html
# Register your models here.
class IBTickerAdmin(admin.ModelAdmin):
	list_display_links = None
	def edit(self, obj):
  		return format_html('<button type="button" class="btn btn-warning btn-xs"><a class="btn" href="/admin/ib_ticker/ibticker/{}/change/">Edit</a></button>', obj.id)

	def delete(self, obj):
  		return format_html('<button type="button" class="btn btn-danger btn-xs"><a class="btn" href="/admin/ib_ticker/ibticker/{}/delete/">Delete</a></button>', obj.id)

	list_display = ('ticker', 'con_id', 'created_at', 'edit', 'delete')



admin.site.register(IBTicker, IBTickerAdmin)