from django.conf import settings
from django.core.mail import EmailMessage


def send_report_email(message):
	subject = 'Portfolio Visualizer'
	from_email = settings.MAIL_FROM
	try:
		message = EmailMessage(subject, message, from_email, 'er.mohittambi@gmail.com')
		message.send()
	except Exception as ex:
		print("Failed to send", ex)