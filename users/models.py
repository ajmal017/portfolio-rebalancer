from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
import pytz, uuid



class User(AbstractUser):
	class Meta:
		verbose_name =_("User")
		verbose_name_plural = _("Users")
	TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

	
	profile_image = models.ImageField(verbose_name=_("Profile Image"), blank=True, null=True, upload_to="profile_image", default="/dummy.png")
	username = models.CharField(verbose_name=_('Username'), max_length=100)
	email = models.EmailField(verbose_name=_('Email'),max_length=200,blank=False,null=False, unique=True)
	dob = models.DateField(verbose_name=_("Date of Birth"), blank=False, null=True)
	phone_number = models.CharField(verbose_name=_("Phone Number"), blank=True, null=True, max_length = 70)
	# country = CountryField(blank_label='(select country)')
	time_zone = models.CharField(max_length=32, choices=TIMEZONES, blank=True, null=False, default='UTC')
	# role = models.CharField(max_length=50, choices=ROLE, blank=False, null=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ('username',)

	def __str__(self):
		return self.username


