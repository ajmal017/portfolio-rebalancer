from rest_framework.permissions import AllowAny
from rest_framework import generics
from modules.configurations.models import *
from modules.payment.models import PaymentDue
from modules.teacher.models import TeacherDocument
from .serializer import *
from api.v1.response_handler import response_handler, serialiser_errors
from django_countries import countries
import pdb 
import pytz, uuid

# class InitialRegistrationView(generics.GenericAPIView):
# 	permission_classes = (AllowAny,)
# 	def get(self, request):
# 		TIMEZONES = pytz.all_timezones
# 		# pdb.set_trace()

# 		music_genre_set = MusicGenre.objects.all() 
# 		instrument_set = Instrument.objects.all()
# 		message = "Initial registration data fetched"
# 		data = {
# 			'music_genre': TeacherMusicGenreSerializer(music_genre_set, many=True).data,
# 			'instrument': InstrumentsSerializer(instrument_set, many=True).data,
# 			'countries': countries._countries,
# 			'timezones': TIMEZONES
# 		}
# 		return response_handler(message=message, data=data)

# class TeacherRegistration(generics.CreateAPIView):
# 	permission_classes = (AllowAny,)
# 	serializer_class = TeacherRegistrationSerializer
# 	def create(self, request, *args, **kwargs):
# 		serializer = self.get_serializer(data=request.data)
# 		if not serializer.is_valid():
# 			error_message = serialiser_errors(serializer)
# 			message = "Registration failed."
# 			return response_handler(message=message, error_message=error_message, code=500)
# 		queryset = super().create(request, *args, **kwargs)
# 		message = "Registration successful"	
# 		return response_handler(message=message, data=queryset.data)
class TeacherProfileUpdateAPIView(generics.UpdateAPIView):
	queryset = Teacher.objects.filter(user__is_superuser=False)
	serializer_class = TeacherProfileUpdateSerializer
	def update(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = self.get_serializer(self.object, data=request.data, partial=True)
		if not serializer.is_valid():
			error_message = serialiser_errors(serializer)
			return response_handler(message=error_message, error_message=error_message, code=500)
		self.object = serializer.save()
		serializer = TeacherProfileSerializer(self.object)
		message = "Details updated successfully"
		return response_handler(message=message, data=serializer.data)

class PaymentHistorylistAPIView(generics.ListAPIView):
	queryset = PaymentDue.objects.all()
	serializer_class = TeacherPaymentHistorySerializer
	def list(self, request):
		queryset = self.get_queryset().filter(booking__teacher=request.user.teacher, status="Complete")
		serializer = self.serializer_class(queryset, many=True)
		message = "Payment history fetched successfully"
		return response_handler(message=message, data=serializer.data)

class TeacherProfilePictureUpdateAPIView(generics.GenericAPIView):
	def post(self, request, pk):
		# pdb.set_trace()
		# pdb.set_trace()
		if request.data.get('profile_image'):

			teacher = Teacher.objects.get(id=pk)
			userid = teacher.user.id
			user = User.objects.get(id=userid)
			user.profile_image = request.data.get('profile_image')
			user.save()
			# teacher.user.profile_image = request.data.get('profile_image')
			# teacher.save()
			serializer = TeacherProfileSerializer(teacher, partial=True)
			message = "Profile Image update successfully"
			return response_handler(message=message, data=serializer.data)
		elif request.data.get('profile_video'):
			teacher = Teacher.objects.get(id=pk)
			teacher.video_file = request.data.get('profile_video')
			teacher.save()
			serializer = TeacherProfileSerializer(teacher, partial=True)
			message = "Profile Video update successfully"
			return response_handler(message=message, data=serializer.data)

		else:
			message = "Profile Image not found"
		return response_handler(message=message, code=400, error_message=message)
class TeacherDocumentDetailUpdateAPIView(generics.UpdateAPIView):
	queryset = TeacherDocument.objects.all()
	serializer_class = TeacherDocumentSerializer
	def update(self, request, *args, **kwargs):
		self.object = self.get_object()
		get_teacher = Teacher.objects.get(id=request.data.get('teacher'))
		get_teacher = get_teacher.user.id
		request.data.pop('teacher')
		request.data.update({'teacher': get_teacher})
		serializer = self.serializer_class(self.object, data=request.data,partial=True)
		print("REquested Data", request.data)
		if not serializer.is_valid():
			print("Error", serializer.errors)
			return response_handler(message=serializer.errors, error_message=serializer.errors, code=400)
		self.object = serializer.save()
		queryset = self.queryset.filter(teacher=self.object.teacher)
		serializer = self.serializer_class(queryset, many=True)
		message = "Teacher Document updated successfully"
		return response_handler(message=message,  data=serializer.data)