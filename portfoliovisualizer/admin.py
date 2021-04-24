from django.contrib import admin
from .models import Target
# Register your models here.



class TargetAdmin(admin.ModelAdmin):
	# def save_related(self, request, form, formsets, change):
	# 	obj = form.instance
	# 	if not obj.role:
	# 		obj.role = "STUDENT"
	# 	if not change:
	# 		obj.password = make_password(obj.password)	
	# 	# make changes to model instance
	# 	obj.save()
		
	# 	super(UserAdmin, self).save_related(request, form, formsets, change)
	list_display = ('ticker', 'target', 'strategy', 'date')



admin.site.register(Target,TargetAdmin)