from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Enquiry(models.Model):
	class Meta:
		verbose_name = "Enquiry"
		verbose_name_plural = "Enquiry"

	first_name = models.CharField(verbose_name=_('First Name'), max_length=30, blank=False, null=False)
	last_name = models.CharField(verbose_name=_('Last Name'), max_length=150, blank=False, null=False)
	email = models.EmailField(verbose_name=_('Email Address'), blank=False, null=False)
	message = models.TextField(verbose_name=_("Message"), blank=False, null=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.email)