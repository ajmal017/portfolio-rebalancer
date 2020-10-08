from django.db import models
from users.models import *
from modules.booking.models import Booking
from django.utils import timezone
from django.utils.timezone import localtime
from random import choice
from django.utils.translation import ugettext_lazy as _
from modules.teacher.models import Teacher
import pdb

def room_number():
	randompass = ''.join([choice('1234567890abcdefghijklmnopqrstuvwxyz') for i in range(10)])
	return randompass.upper()

class ChatRoom(models.Model):
	class Meta:
		verbose_name_plural = _('Chat Room')

	teacher = models.ForeignKey(Teacher, null=True, blank=True,on_delete=models.CASCADE)
	student = models.ForeignKey(User, null=True, blank=True,on_delete=models.CASCADE, related_name="chat_room_student")
	room_number = models.CharField(verbose_name=_('Room Number'), max_length=20, default=room_number)
	created_at = models.DateTimeField(auto_now=True)
	# booking = models.OneToOneField(Booking, related_name="booking_room_number", null=True, blank=True, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.room_number) + "(Student--" + str(self.student.username) + ")" + "(Teacher--" + str(self.teacher.user.username) + ")"

	def __unicode__(self):
		return str(self.room_number)

	@property
	def group_name(self):
		return "room-%s" % self.id

class ChatMessage(models.Model):
	class Meta:
		ordering = ('-message_at',)
	TEXT = 'TEXT'
	IMAGE = 'IMAGE'
	DOCUMENT = 'DOCUMENT'

	CHOICES = (
		(TEXT,_('Text')),
		(IMAGE,_('Image')),
		(DOCUMENT,_('Document')))

	sender = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	receiver = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="message_receiver")
	room_id = models.ForeignKey(ChatRoom, null=True, blank=True, on_delete=models.CASCADE)
	message = models.TextField(verbose_name=_('Chat Meassage'), default="")
	message_type = models.CharField(verbose_name=_('Meassage Type'), max_length=10, default=TEXT, choices=CHOICES)
	media_url = models.CharField(verbose_name=_('Media Url'), max_length=200, default="")
	message_at = models.DateTimeField(auto_now=True)
	seen = models.BooleanField(default=False)

	def __str__(self):
		return str(self.id)

	def __unicode__(self):
		return str(self.id)

class ChatMedia(models.Model):
	class Meta:
		verbose_name = _('Chat Media')
		verbose_name_plural = _('Chat Medias')
	file = models.FileField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.id)
	