# from rest_framework.authtoken.models import Token
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import User
from django.contrib.auth.models import Group
from .forms import UserAdminForm
from django.db.models import Q
# Register your models here.

class UserAdmin(admin.ModelAdmin):
	# def save_related(self, request, form, formsets, change):
	# 	obj = form.instance
	# 	if not obj.role:
	# 		obj.role = "STUDENT"
	# 	if not change:
	# 		obj.password = make_password(obj.password)	
	# 	# make changes to model instance
	# 	obj.save()
		
	# 	super(UserAdmin, self).save_related(request, form, formsets, change)
	list_display = ('username', 'email', 'dob', 'phone_number', 'is_active')
	fields = ('profile_image','username', 'email', 'dob', 'language', 'country', 'time_zone', 'password', 'phone_number', 'is_active')
	search_fields = ('username', 'email', 'dob', )
	form =  UserAdminForm
	def get_readonly_fields(self, request, obj=None):
		if obj:
			return ["password"]
		else:
			return []
	def get_queryset(self, request):
		qs = super(UserAdmin, self).get_queryset(request)
		return qs.exclude(is_superuser=True)
		# return qs.filter(Q(is_superuser=False, role="STUDENT") | Q(is_superuser=False, role="STUDENT-TEACHER"))
		# return qs.filter(teacher__isnull=True, is_superuser=False)

admin.site.unregister(Group)
# admin.site.unregister(Token)
admin.site.register(User,UserAdmin)
