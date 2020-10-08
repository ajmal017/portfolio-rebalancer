from django.contrib import admin
from .models import Enquiry
# Register your models here.


class EnquiryAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'email', 'message')
	def has_add_permission(self, obj):
		return False
	
admin.site.register(Enquiry, EnquiryAdmin)