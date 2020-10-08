from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
import pdb
import pytz, uuid
from django_countries.fields import CountryField
# class Role(models.Model):
#     STUDENT = 1
#     TEACHER = 2
#     ROLE_CHOICES = {
#         (STUDENT, 'student'),
#         (TEACHER, 'teacher'),
#     }

#     id = models.PositiveIntegerField(choices = ROLE_CHOICES, primary_key = True)

#     def __str__(self):
#         return self.get_id_display()


class User(AbstractUser):
	class Meta:
		verbose_name =_("Student")
		verbose_name_plural = _("Students")
	TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

	ROLE = (
		('STUDENT', 'Student'),
		('TEACHER', 'Teacher'),
		('STUDENT-TEACHER', 'Student-Teacher')
	)
	LANGUAGE = (
		('ENGLISH', 'English'),
		('MANDARIN', 'Mandarin')
	)
	profile_image = models.ImageField(verbose_name=_("Profile Image"), blank=True, null=True, upload_to="profile_image", default="/dummy.png")
	username = models.CharField(verbose_name=_('Username'), max_length=100)
	email = models.EmailField(verbose_name=_('Email'),max_length=200,blank=False,null=False, unique=True)
	dob = models.DateField(verbose_name=_("Date of Birth"), blank=False, null=True)
	phone_number = models.CharField(verbose_name=_("Phone Number"), blank=True, null=True, max_length = 70)
	language = models.CharField(verbose_name=_("Language"),choices=LANGUAGE, max_length=30, blank=True, null=False)
	# country = CountryField(blank_label='(select country)')
	country = CountryField(blank=True, null=False)
	time_zone = models.CharField(max_length=32, choices=TIMEZONES, blank=True, null=False, default='UTC')
	role = models.CharField(max_length=50, choices=ROLE, blank=False, null=True)
	is_active = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ('username',)

	def __str__(self):
		return self.username

	@property
	def is_teacher(self):
		return hasattr(self, 'teacher')



class Teachers(User):

	class Meta:
		verbose_name =_("Teacher")
		verbose_name_plural = _("Teacher")
		proxy = True
	# def save(self, *args, **kwargs):
	# 	if not self.is_superuser:
	# 		if self.role:
	# 			self.role = "TEACHER"
	# 		else:
	# 			self.role = "STUDENT"
	# 	super(User, self).save(*args, **kwargs)

