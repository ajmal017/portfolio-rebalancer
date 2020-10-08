from rest_framework import generics 
from api.v1.response_handler import response_handler, serialiser_errors
from modules.booking.models import Notification, Media
from .serializer import *
import pdb

class BookingView(generics.GenericAPIView):
	def get(self, request):
		try:
			query = {k: request.GET.get(k) for k in request.GET }
			queryset =  request.user.teacher.booking_set.order_by('-id').filter(**query).exclude(booking_status="REJECT")
			if queryset.exists():
				serializer = TeacherBookingListSerializers(queryset, many=True)
				message = 'Bookings list fetched successfully'
				return response_handler(message = message, data=serializer.data)
			else:
				message = 'No booking found'
				return response_handler(message=message)
		except Exception as ex:
			message = 'Something went wrong.'
			return response_handler(message = message, code=500, error_message=str(ex))
class MediaListAPIView(generics.GenericAPIView):
	def get(self, request):
		shared_video =Media.objects.filter(booking__teacher=request.user.teacher, shared_by="TEACHER").order_by('-id')
		received_video =Media.objects.filter(booking__teacher=request.user.teacher, shared_by="STUDENT").order_by('-id')
		shared_video = TeacherShareVideoMediaListSerializer(shared_video, many=True).data
		received_video = TeacherShareVideoMediaListSerializer(received_video, many=True).data
		message = "Media list fetched successfully"
		return response_handler(message=message, data={"shared_video": shared_video, "received_video":received_video})
class UpdateBookingStatusView(generics.UpdateAPIView):
	queryset = Booking.objects.all()
	serializer_class = TeacherBookingListSerializers
	def update(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = self.get_serializer(self.object, data=request.data, partial=True)
		if not serializer.is_valid():
			error_message = serialiser_errors(serializer)
			return response_handler(message=error_message, error_message=error_message, code=500)
		self.object = serializer.save()
		SUCCESS_MESSAGE = {
		  "ACTIVE": "Booking request accepted",
		  "REJECT": "Booking request rejected"
		}
		message = SUCCESS_MESSAGE[request.data.get('booking_status').upper()]
		# notification = Notification(sender=request.user, receiver=obj.teacher.user, title="New Booking", note=obj.message)
		if self.object.booking_status == "ACTIVE":
			notification = Notification(sender=request.user, receiver=self.object.student, title="Booking Accepted", note=self.object.booking_message)
		else:
			notification = Notification(sender=request.user, receiver=self.object.student, title="Booking Rejected", note=self.object.booking_message)
		notification.content_object = self.object
		notification.save()

		return response_handler(message=message, data=serializer.data)