from django.contrib import admin
from .models import Target
# Register your models here.
class TargetAdmin(admin.ModelAdmin):
	list_display = ('ticker', 'target', 'strategy')




admin.site.register(Target, TargetAdmin)