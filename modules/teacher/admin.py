from django.contrib import admin
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from .models import Teacher, TeacherDocument, TeacherExperience
from .forms import TeacherAdminForm
from users.models import User, Teachers
from users.admin import UserAdmin
from .models import Teacher
import pdb
# Register your models here.

class CertificateInline(admin.StackedInline):
	model = TeacherDocument
	# extra = 2
	extra = 1
	# max_num = 5
	max_num = 1

class TeacherExperience(admin.StackedInline):
	model = TeacherExperience
	extra = 2
	max_num = 5

class TeacherInline(admin.StackedInline):
	model = Teacher
	verbose_name = "More Information"
	verbose_name_plural = "More Information"
	exclude = ['pke',]
	extra = 1
	can_delete = False

class UserAdmin(admin.ModelAdmin):
	# def save_model(self, request, obj, form, change):
	# 	# pdb.set_trace()
	# 	if not hasattr(obj, 'teacher'):
	# 		super(UserAdmin, self).save_model(request, obj, form, change)
	# 		# Teacher.objects.create(user=obj)
	# 		teacher = Teacher(user=obj)
	# 		teacher.save()
	# def save_model(self, request, obj, form, change):
	# 	pdb.set_trace()
	# 	if not change:
	# 		if request.POST['username'] and request.POST['email'] and request.POST['dob'] and request.POST['phone_number']
	# 	super(UserAdmin, self).save_model(request, obj, form, change)
	# def save_model(self, request, obj, form, change):
	# 	if not change:
	# 		obj.role = "TEACHER"
	# 		obj.password = make_password(obj.password)	
	# 		super().save_model(request, obj, form, change)
	def save_related(self, request, form, formsets, change):
		obj = form.instance
		
		if not change:
			obj.role = "TEACHER"
			obj.password = make_password(obj.password)	
		# make changes to model instance
		obj.save()
		if not hasattr(obj, 'teacher'):
			print("Ok please create teacher")
			Teacher.objects.create(user=obj)
		super(UserAdmin, self).save_related(request, form, formsets, change)
			
	list_display = ('username','email', 'phone_number', 'is_active', 'get_verified')
	def get_verified(self, obj):
		teacher = Teacher.objects.get(user=obj)
		return teacher.is_verified
	inlines = [TeacherInline, CertificateInline, TeacherExperience]
	# inlines = [TeacherInline, TeacherExperience]
	# readonly_fields = ('password',)
	def get_readonly_fields(self, request, obj=None):
		if obj:
			return ["password"]
		else:
			return []
	fields = ['profile_image', 'username','email', 'dob', 'language', 'country', 'time_zone', 'password', 'phone_number', 'is_active']
	# readonly_fields=('password',)
	def get_queryset(self, request):
		qs = super(UserAdmin, self).get_queryset(request)
		for q in qs:
			if not hasattr(q, 'teacher'):
				qs = qs.exclude(id=q.id)
		# return qs.filter(Q(is_superuser=False, role="TEACHER") | Q(role="STUDENT-TEACHER"))
		return qs.filter(is_superuser=False)

admin.site.register(Teachers, UserAdmin)
admin.site.unregister(Token)


 
# class TeacherInline(admin.modelAdmin):
	# model = Teacher
	# fields = ('experience ', 'level')
	# inlines = [UserInline]
# class TeacherInline(admin.StackedInline):
    # model = Teacher
	# extra = 1
# class ExtendedProductAdmin(UserAdmin):
    # inlines = UserAdmin.inlines + [TeacherInline]

# class TeacherAdmin(admin.ModelAdmin):
# 	list_display=('experience', 'level')
# 	inlines = [UserInline, CertificateInline]
	# form = TeacherAdminForm
	# fields = ('username', 'email', 'dob', 'password', 'phone_number','profile_image', 'gender', 'level', 'city', 'experience', 'country', 'time_zone', 'language', 'video_file', 'music_genres','instruments', 'short_introduction', 'about', 'is_active', 'is_verified')
	# search_fields = ('username', 'email', 'dob', )
	# def get_queryset(self, request):
	# 	qs = super(TeacherAdmin, self).get_queryset(request)
	# 	return qs.filter(is_superuser=False)


# class TeacherAdmin(admin.ModelAdmin):
# 	list_display = ('username','email',)
# 	inlines = [TeacherInline,]

# admin.site.register(UserProxy, ExtendedProductAdmin)


# admin.site.register(Teacher,TeacherAdmin)

