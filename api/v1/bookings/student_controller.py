from rest_framework import generics 
from api.v1.response_handler import response_handler, serialiser_errors
from modules.booking.models import Notification, Media, Booking
from modules.configurations.models import Setting
from .serializer import *
from modules.teacher.models import Teacher
import pdb

class BookingCreateAPIView(generics.GenericAPIView):
	def post(self, request, *args, **kwargs):
		serializer = BookingCreateSerializer(data=request.data)
		if not serializer.is_valid():
			error_message = serialiser_errors(serializer)
			message = "Failed to schedule booking"
			return response_handler(message=message, error_message=error_message, code=500)
		obj = serializer.save()
		admin_commission = Setting.objects.filter(configuration=Setting.ADMIN_COMMISSION)
		if admin_commission.exists():
			admin_commission = admin_commission.first()
			admin_commission = obj.teacher.price_per_lesson * admin_commission.amount/100
			price = obj.teacher.price_per_lesson 
		else:
			admin_commission = obj.teacher.price_per_lesson * 18/100
			price = obj.teacher.price_per_lesson

		booking = Booking.objects.get(id=obj.id)
		booking.price = price
		booking.admin_commission = admin_commission
		booking.save()
		message = "Your booking is successfully send to {teachername}".format(teachername=booking.teacher.user.username)
		notification = Notification(sender=request.user, receiver=obj.teacher.user, title="New Booking", note=obj.message)
		notification.content_object = obj
		notification.save()
		serializer= BookingCreateSerializer(obj).data
		return response_handler(message=message, data=serializer)

class MediaListAPIView(generics.GenericAPIView):
	def get(self, request):
		# all_media =Media.objects.filter(booking__student=request.user).order_by('-id')
		shared_video =Media.objects.filter(booking__student=request.user, shared_by="STUDENT").order_by('-id')
		received_video =Media.objects.filter(booking__student=request.user, shared_by="TEACHER").order_by('-id')
		
		shared_video = StudentShareVideoMediaListSerializer(shared_video, many=True).data
		received_video = StudentShareVideoMediaListSerializer(received_video, many=True).data
		message = "Media list fetched successfully"
		return response_handler(message=message, data={"shared_video": shared_video, "received_video":received_video})

class BookingView(generics.GenericAPIView):
	def get(self, request):
		try:
			query = {k: request.GET.get(k) for k in request.GET }
			queryset =  request.user.booking_set.order_by('-id').filter(**query)
			if queryset.exists():
				serializer = StudentBookingListSerializers(queryset, many=True)
				message = 'Bookings list fetched successfully'
				return response_handler(message = message, data=serializer.data)
			else:
				message = 'No booking found'
				return response_handler(message=message)
		except Exception as ex:
			message = 'Something went wrong.'
			return response_handler(message = message, code=500, error_message=str(ex))