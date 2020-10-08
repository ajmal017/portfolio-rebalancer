from django.db import models
from django.utils.translation import ugettext_lazy as _
from users.models import User
from django.db.models.signals import pre_save, post_save
# from modules.configurations.models import MusicGenre
import pytz, uuid
# Create your models here.

# to = "users.User"

class Teacher(models.Model):
	class Meta:
		verbose_name =_("Teacher")
		verbose_name_plural = _("Teachers")

	TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

	GENDER_CHOICES = (
		('MALE', 'Male'),
		('FEMALE', 'Female')
	)
	LEVEL_CHOICES = (
		('BEGINNER', 'Beginner'),
		('INTERMEDIATE', 'Intermediate'),
		('ADVANCED', 'Advanced')
	)
	# LANGUAGE = (
	# 	('ENGLISH', 'English'),
	# 	('MANDARIN', 'Mandarin')
	# )
	user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE, unique=True)
	gender = models.CharField(verbose_name=_("Gender"), choices=GENDER_CHOICES, blank=True, null=True, max_length=100)
	level = models.CharField(verbose_name=_("Level Taught"), choices=LEVEL_CHOICES, blank=True, null=True, max_length=100)
	# country = models.CharField(verbose_name=_("Country"), max_length=30, blank=True, null=True)
	# city = models.CharField(verbose_name=_("City"), max_length=50, blank=True, null=True)
	experience = models.FloatField(verbose_name=("Total Experience"), blank=True, null=True)
	# time_zone = models.CharField(max_length=32, choices=TIMEZONES, blank=True, null=True, default='UTC')
	# language = models.CharField(verbose_name=_("Language"),choices=LANGUAGE, max_length=30, blank=True, null=True)
	video_file= models.FileField(verbose_name=_("Teacher Video"), upload_to="teacher_video", blank=True, null=True)
	short_introduction = models.TextField(verbose_name=("Teacher Introduction"), blank=True, null=True)
	about = models.TextField(verbose_name=("About Me"), blank=True, null=True)
	music_genres = models.ManyToManyField(to="configurations.MusicGenre", verbose_name=_("Music Genres"), blank=True, null=True)
	# instruments = models.ManyToManyField(to="configurations.Instrument", verbose_name=_("Instruments Taught"), blank=True, null=True)
	price_per_lesson = models.FloatField(verbose_name=_("Price Per Lesson"), default=0,  blank=True, null=True)
	is_verified = models.BooleanField(verbose_name=("Is Verified ?"), default=False)

	# def save(self, *args, **kwargs):
	# 	self.role = "TEACHER"
	# 	super(Teacher, self).save(*args, **kwargs)
	def __str__(self):
		return self.user.username

	@property
	def is_student(self):
		return hasattr(self, 'user')

def new_document_created(sender, instance, created, **kwargs):
	if created:  
		try:
			teacher_document =  TeacherDocument.objects.filter(teacher=instance.user)
			if not teacher_document.exists():
				TeacherDocument.objects.create(teacher=instance.user)
		except Exception as ex:
			print(ex)

        
post_save.connect(new_document_created, sender=Teacher)

class TeacherExperience(models.Model):
	teacher = models.ForeignKey(to="users.User", verbose_name=("Teacher"), on_delete=models.CASCADE, blank=False, null=True)
	instruments = models.ForeignKey(to="configurations.Instrument", verbose_name=_("Instruments Taught"), on_delete=models.CASCADE,  blank=False, null=True)
	experience = models.FloatField(verbose_name=("Instrument Experience"), blank=False, null=True)


class TeacherDocument(models.Model):
	class Meta:
		verbose_name =_("Document")
		verbose_name_plural = _("Documents")
	teacher = models.ForeignKey(to="users.User", verbose_name=("Teacher"), on_delete=models.CASCADE, blank=False, null=True)
	certificate_1 = models.FileField(verbose_name='Certificate Record 1', blank=True, null=True, upload_to='teacher_document', default=('/certificate_1.png'))
	certificate_2 = models.FileField(verbose_name='Certificate Record 2', blank=True, null=True, upload_to='teacher_document', default=('/certificate_2.png'))
	certificate_3 = models.FileField(verbose_name='Certificate Record 3', blank=True, null=True, upload_to='teacher_document', default=('/certificate_3.png'))
	certificate_4 = models.FileField(verbose_name='Certificate Record 4', blank=True, null=True, upload_to='teacher_document', default=('/certificate_4.png'))
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)