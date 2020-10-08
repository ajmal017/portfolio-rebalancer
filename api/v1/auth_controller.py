from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from api.v1.response_handler import response_handler, serialiser_errors
from api.v1.teachers.serializer import *
from api.v1.students.serializer import *
from .common_serializers import *
from rest_framework import generics
from modules.configurations.models import Teacher
from modules.configurations.tasks import send_activation_email, send_reset_password_link
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django_countries import countries
import pytz, uuid
import pdb

# class StudentRegistration(generics.CreateAPIView):
# 	permission_classes = (AllowAny,)
# 	serializer_class = StudentRegistrationSerializer
# 	def create(self, request, *args, **kwargs):
# 		serializer = self.get_serializer(data=request.data)
# 		if not serializer.is_valid():
# 			error_message = serialiser_errors(serializer)
# 			message = "Registration failed."
# 			return response_handler(message=message, error_message=error_message, code=500)
# 		queryset = super().create(request, *args, **kwargs)
# 		message = "Registration successful"	
# 		return response_handler(message=message, data=queryset.data)


class InitialRegistrationView(generics.GenericAPIView):
	permission_classes = (AllowAny,)
	def get(self, request):
		TIMEZONES = pytz.all_timezones
		Country = []
		TIMEZONE = []
		for country in countries._countries:
			Country.append({'country_code': country, 'country_name': countries._countries[country]})
		for timezone in TIMEZONES:
			TIMEZONE.append({'time_zone_code': timezone, 'time_zone_name': timezone})
		music_genre_set = MusicGenre.objects.all() 
		instrument_set = Instrument.objects.all()
		message = "Initial registration data fetched"
		data = {
			'music_genre': TeacherMusicGenreSerializer(music_genre_set, many=True).data,
			'instrument': InstrumentsSerializer(instrument_set, many=True).data,
			'countries': Country,
			'timezones': TIMEZONE
		}
		return response_handler(message=message, data=data)
		
class SignUpAPIView(generics.CreateAPIView):
	permission_classes = (AllowAny,)
	serializer_class = UserRegistrationSerializer
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		if not serializer.is_valid():
			error_message = serialiser_errors(serializer)
			message = _("Registration failed")
			return response_handler(message=message, error_message=error_message, code=500)
		queryset = super().create(request, *args, **kwargs)
		send_activation_email.delay(self.request.scheme, self.request.get_host(), queryset.data.get('id'))
		message = _("Registered successfully, An email has been sent to your registered email id. please verify email before login")	
		return response_handler(message=message, data=queryset.data)


class Login(APIView):
	permission_classes = (AllowAny,)
	def post(self, request):
		email = request.data.get('email', None)
		password = request.data.get('password', None)
		if email and password:
			if "@" in email:
				serializer = UserLoginSerializer(data=request.data)
				# pdb.set_trace()
				if serializer.is_valid():
					if request.data.get('role') == 'TEACHER':
						user = User.objects.filter(Q(email__iexact=request.data.get('email'), role="TEACHER") | Q(email__iexact=request.data.get('email'), role="STUDENT-TEACHER"))
						if not user.exists():
							message = _("Provide valid credentials")
							return response_handler(message=message, code=400, error_message=message)
					else:
						if request.data.get('role') == 'STUDENT':
							user = User.objects.filter(Q(email__iexact=request.data.get('email'), role="STUDENT") | Q(email__iexact=request.data.get('email'), role="STUDENT-TEACHER"))
							# User.objects.filter(Q(income__gte=5000) | Q(income__isnull=True))
							# pdb.set_trace()
							if not user.exists():
								message = _("Provide valid credentials")
								return response_handler(message=message, code=400, error_message=message)
					# if user.suspended == True:
					# 	message = "You are suspended by the admin, please contact to admin"
					# 	return response_handler(message=message, code=400, error_message=message)
					
					user = user.first()
					# pdb.set_trace()
					if request.data.get('role') == 'TEACHER':
						# pdb.set_trace()
						if hasattr(user, 'teacher'):
							if not user.is_active:
								# otp_code = random_code()
								try:
									# worker_activation_email.delay(user.id, otp_code)
									# UserOtp.objects.create(user=user, otp=otp_code)
									message = _("Your account is not active")
									return response_handler(message=message, code=401,
															data={'is_active': False}, error_message=message)
								except:
									pass
							teacher = Teacher.objects.get(user=user)
							# if teacher.is_verified == False:
							# 	message = "Admin verification is required, please wait."
							# 	return response_handler(message=message, code=400, error_message=message)
							user_serializer = TeacherProfileSerializer(teacher).data
						else:
							message = _("Provide valid credentials")
							return response_handler(message=message, code=400, error_message=message)
					# elif hasattr(user, 'customer'):
					# 	user_serializer = CustomerProfileSerializer(user.customer).data
					else:
						if request.data.get('role') == 'STUDENT':
							if user.is_teacher:
								user_serializer = TeacherProfileSerializer(user.teacher).data
							else:
								user_serializer = StudentProfileSerializer(user).data
						else:
							message = _("Provide valid credentials")
							return response_handler(message=message, code=400, error_message=message)
						# if request Header is None then elegible for login
					if user.is_active:
						message = _("login Successful")
						return response_handler(message=message, data=user_serializer)
					else:
						# print("OTP")
						# otp_code = random_code()
						try:
							if user.is_teacher:
								# worker_activation_email.delay(user.id, otp_code)
								print("Send Activation Mail to teacher")
							else:
								# customer_activation_email.delay(user.id, otp_code)
								print("Send Activation Mail to student")
						except:
							pass
						# UserOtp.objects.create(user=user, otp=otp_code)
						message = _("Your account is not active")
						return response_handler(message=message, code=401, data={'is_active': False}, error_message=message)
				else:
					error_message = serialiser_errors(serializer)
					message = _('Login failed, Please check error message')
					return response_handler(message=message, error_message=error_message, code=500)
		else:
			message = _("Invalid login details")
			return response_handler(message=message, error_message=message, code=500)

class ActivateAccountAPIView(generics.GenericAPIView):
	# print("Hello")
	permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):
		# print("Hello")
		uidb64 = request.data.get('id')
		token = request.data.get('token')
		assert uidb64 is not None and token is not None
		try:
			uid = urlsafe_base64_decode(uidb64)
			user = User._default_manager.get(pk=uid)
		except (TypeError, ValueError, OverflowError, User.DoesNotExist):
			user = None
		if user:
			user.is_active = True
			user.save()
			message = _("Account activated successfully, you can login now")
			return response_handler(message=message)
		else:
			message = _("Something went wrong")
			return response_handler(message=message, error_message=message, code=500)

class ForgetPasswordAPIView(generics.GenericAPIView):
	def post(self, request):
		email = request.data.get('email', None)
		users = User.objects.filter(email__iexact=email)

		if users.exists():
			user = users.first()
			send_reset_password_link(request, user.id)
			message = _("Please check your email for reseting password instructions")
			return response_handler(message=message)
		else:
			message = _("Email Address not exists")
			return response_handler(message=message, error_message=message, code=500)

class ResetUserPasswordView(generics.GenericAPIView):
	def get(self, request, uidb64=None, token=None, *args, **kwargs):
		assert uidb64 is not None and token is not None
		try:
			uid = urlsafe_base64_decode(uidb64)
			user = User._default_manager.get(pk=uid)
		except (TypeError, ValueError, OverflowError, User.DoesNotExist):
			user = None
		if user:
			return render(request, "reset-password.html", {"uidb": uidb64, "token": token})
		else:
			return HttpResponseRedirect(reverse_lazy('home'))

	def post(self, request, uidb64=None, token=None, *args, **kwargs):
		try:
			uid = urlsafe_base64_decode(uidb64)
			user = User._default_manager.get(pk=uid)
		except (TypeError, ValueError, OverflowError, User.DoesNotExist):
			user = None
		if request.POST.get('password') != "":
			if request.POST.get('password') == request.POST.get('confirm_password'):
				if user is not None and default_token_generator.check_token(user, token):
					user.set_password(request.POST.get('password'))
					user.save()
					messages.success(request, "Password has been reset")
					return HttpResponseRedirect(reverse_lazy('home'))
				else:
					messages.error(request, "The reset Password link is no longer valid")
					return render(request, 'reset-password.html')
			else:
				messages.error(request, "Password mismatched !")
				return render(request, 'reset-password.html')
		else:
			messages.error(request, "Password can not be blank.")
			return render(request, 'reset-password.html')

class RoleUpdateAPIView(generics.GenericAPIView):
	def post(self, request, *args, **kwargs):
		# pdb.set_trace()
		if not request.user.is_teacher:
			user = User.objects.get(id=request.user.id)
			user.role = 'STUDENT-TEACHER'
			user.save()
			teacher = Teacher(user=user)
			teacher = teacher.save()
			serializer = TeacherProfileSerializer(teacher).data
		else:
			# user = User.objects.filter(id=request.user.id).update(role='STUDENT-TEACHER')
			# pdb.set_trace()
			# print("else")
			user = User.objects.get(id=request.user.id)
			serializer = TeacherProfileSerializer(user.teacher).data
		message = _("Role updated successfully")
		return response_handler(message=message, data=serializer)

class ChangePassword(generics.GenericAPIView):
	def post(self, request):
		old_password = request.data.get('old_password', None)
		new_password = request.data.get('new_password')
		user = request.user
		if user.check_password(old_password):
			user.set_password(new_password)
			user.save()
			if user.is_teacher:
				user_serializer = TeacherProfileSerializer(user.teacher).data
			else:
				user_serializer = StudentProfileSerializer(user).data
			message = _("Password Changed successfully")
			return response_handler(message=message, data=user_serializer)
		else:
			message = _("Wrong old password")
			return response_handler(message=message, code=500, error_message=message)

