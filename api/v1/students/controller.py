from rest_framework.permissions import AllowAny
from rest_framework import generics 
from modules.payment.models import PaymentHistory
from api.v1.response_handler import response_handler, serialiser_errors
from .serializer import *
from users.models import User
# from .serializer import *
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
class StudentProfileUpdateAPIView(generics.UpdateAPIView):
	queryset = User.objects.filter(is_superuser=False)
	serializer_class = StudentProfileUpdateSerializer
	def update(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = self.get_serializer(self.object, data=request.data, partial=True)
		if not serializer.is_valid():
			return response_handler(message=serializer.errors, error_message=serializer.errors, code=400)
		self.object = serializer.save()
		message = "Details updated successfully"
		return response_handler(message=message, data=serializer.data)

class PaymentHistorylistAPIView(generics.ListAPIView):
	queryset = PaymentHistory.objects.all()
	serializer_class = StudentPaymentHistorySerializer
	def list(self, request):
		queryset = self.get_queryset().filter(booking__student=request.user)
		serializer = self.serializer_class(queryset, many=True)
		message = "Payment history fetched successfully"
		return response_handler(message=message, data=serializer.data)

class StudentProfilePictureUpdateAPIView(generics.GenericAPIView):
	def post(self, request, pk):
		# pdb.set_trace()
		# pdb.set_trace()
		if request.data.get('profile_image'):

			user = User.objects.get(id=pk)
			user.profile_image = request.data.get('profile_image')
			user.save()
			serializer = StudentProfileSerializer(user, partial=True)
			message = "Profile Image update successfully"
			return response_handler(message=message, data=serializer.data)
		else:
			message = "Profile Image not found"
		return response_handler(message=message, code=400, error_message=message)