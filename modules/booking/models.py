from django.db import models
from django.utils.translation import ugettext_lazy as _
from users.models import User
from django.utils.encoding import smart_str
from modules.teacher.models import Teacher
from languages.fields import LanguageField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.


class Booking(models.Model):
	BOOKINGSTATUS = (
		# Self Cancel ?
		('PENDING', 'Pending'),
		('ACTIVE','Active'),
		('REJECT','Reject'),
		('COMPLETED', 'Completed')
	)
	BOOKINGPAYMENTSTATUS = (
		("PENDING",'Pending'),
		("SUCCESS",'Success')
	)
	student = models.ForeignKey(User, verbose_name=('Student'), blank=False, null=False, on_delete=models.CASCADE)
	teacher = models.ForeignKey(Teacher, verbose_name=_('Teacher'), blank=False, null=False, on_delete=models.CASCADE)
	country = models.CharField(verbose_name=_("Country"), max_length=60)
	language = models.CharField(verbose_name=_("Language"), max_length=60)
	date_of_upload = models.DateField(verbose_name=_("Video upload Date"))
	message = models.TextField(verbose_name=_('Message'))
	booking_status = models.CharField(verbose_name=_('Booking Status'), max_length=50, default='PENDING', choices=BOOKINGSTATUS)
	payment_status = models.CharField(verbose_name=_('Payment Status'), max_length=50, default="PENDING", choices=BOOKINGPAYMENTSTATUS)
	booking_message = models.TextField(verbose_name=_('Booking Status Message'), blank=True, null=False)
	student_satisfy = models.BooleanField(verbose_name=_("Student Satisfy"), default=False)
	teacher_satisfy = models.BooleanField(verbose_name=_("Teacher Satisfy"), default=False)
	price = models.FloatField(verbose_name=_("Price"), blank=True, null=True)
	admin_commission = models.FloatField(verbose_name=_("Admin commission"), blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.id)


class Media(models.Model):
	SHARED_BY = (
		("STUDENT", 'Student'),
		("TEACHER", 'Teacher')
	)
	class Meta:
		verbose_name = "Media"
		verbose_name_plural = "Media"

	# booking
	booking = models.ForeignKey(Booking, verbose_name=_("Booking"), blank=False, null=True,on_delete=models.CASCADE)
	document = models.FileField(verbose_name=_("Document"),upload_to="media-doc", blank=True, null=False)
	video_file= models.FileField(verbose_name=_("Video"), upload_to="media-videos", blank=True, null=False)
	description = models.TextField(verbose_name=_("Additional Information"), blank=True, null=False)
	shared_by = models.CharField(verbose_name=_('Shared By'), max_length=50, choices=SHARED_BY)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Notification(models.Model):
	class Meta:
		verbose_name = ('Notification')
		verbose_name_plural = ('Notifications')

	receiver = models.ForeignKey(verbose_name=_('User to be notified'), to="users.User", null=True, blank=True, on_delete=models.SET, related_name="receivers")
	sender = models.ForeignKey(verbose_name=_('User who sent notification'), to="users.User", null=True, blank=True, on_delete=models.SET, related_name="senders")
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	# template = models.ForeignKey(NotificationTemplate, null=True, blank=True, on_delete=models.SET_NULL)
	title = models.TextField(verbose_name=_("Notification Title"), blank=True, null=False)
	note = models.TextField(verbose_name=_("Notification Content"), blank=True, null=False)
	seen = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return smart_str("%s-%s"%(self.receiver.username, self.content_object)) 