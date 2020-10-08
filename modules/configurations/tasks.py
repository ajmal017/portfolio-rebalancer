from django.conf import settings
from .models import EmailTemplate
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from celery.decorators import task
from django.utils.encoding import force_bytes
from django.urls import reverse_lazy
from users.models import User
from modules.booking.models import Booking
import pdb

@task(name='Send email to workers for activating account')
def send_activation_email(scheme, host,  userId):
	text_content = 'Account Activation Email'
	subject = 'Email Activation'
	users = User.objects.filter(pk=userId)
	if users.exists():
		user = users.first()
		if not user.is_teacher:
			templates = EmailTemplate.objects.filter(template_name=EmailTemplate.STUDENT_REGISTRATION)
		else:
			templates = EmailTemplate.objects.filter(template_name=EmailTemplate.TEACHER_REGISTRATION)
		if templates.exists():
			template = templates.first()
			from_email = settings.MAIL_FROM
			try:
				# kwargs = {
				# "uidb64": urlsafe_base64_encode(force_bytes(user.pk)),
				# "token": default_token_generator.make_token(user)
				# }
				# activation_url = reverse_lazy("activation", kwargs=kwargs)
				# http://127.0.0.1:8000/verifyemail?id=xyz&token=123s1df564ds6f5
				activation_url = "/verifyemail?id=" + urlsafe_base64_encode(force_bytes(user.pk)) + "&token=" + default_token_generator.make_token(user)
				reset_url = "{0}://{1}{2}".format(scheme, host, activation_url)
				# pdb.set_trace()
				recipients = [user.email]
				html_message = template.email_content.format(username=user.username,url=reset_url)
				message = EmailMessage(subject, html_message, settings.MAIL_FROM, [user.email])
				# pdb.set_trace()
				message.content_subtype = "html"
				message.send()
			except Exception as ex:
				print(ex)

def send_reset_password_link(request, userId):
	text_content = 'Account Forget Password Email'
	subject = 'Forget Password'
	users = User.objects.filter(pk=userId)
	if users.exists():
		user = users.first()
		templates = EmailTemplate.objects.filter(template_name=EmailTemplate.FORGOT_PASSWORD)
		if templates.exists():
			template = templates.first()
			from_email = settings.MAIL_FROM
			try:
				kwargs = {
				"uidb64": urlsafe_base64_encode(force_bytes(user.pk)),
				"token": default_token_generator.make_token(user)
				}
				change_password_url = reverse_lazy("reset-password", kwargs=kwargs)
				reset_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), change_password_url)
				# pdb.set_trace()
				recipients = [user.email]
				html_message = template.email_content.format(username=user.username,url=reset_url)
				message = EmailMessage(subject, html_message, settings.MAIL_FROM, [user.email])
				# pdb.set_trace()
				message.content_subtype = "html"
				message.send()
			except Exception as ex:
				print(ex)

@task(name='Send payment success notify')
def payment_success_notify(bookingId, amount):
	text_content = 'Booking Payment Success'
	subject = 'Booking Payment'
	booking = Booking.objects.filter(pk=bookingId)
	# pdb.set_trace()
	if booking.exists():
		booking = booking.first()
		templates = EmailTemplate.objects.filter(template_name=EmailTemplate.STUDENT_PAYMENT_SUCCESS)
		if templates.exists():
			template = templates.first()
			from_email = settings.MAIL_FROM
			try:
				recipients = [booking.student.email]
				html_message = template.email_content.format(username=booking.student.username,amount=amount)
				message = EmailMessage(subject, html_message, settings.MAIL_FROM, [booking.student.email])
				message.content_subtype = "html"
				message.send()
				teacher_message = "Booking confirmed by the {student}".format(student=booking.student.username)
				message = EmailMessage(subject, teacher_message, settings.MAIL_FROM, [booking.teacher.user.email])
				message.content_subtype = "html"
				message.send()
			except Exception as ex:
				print(ex)
