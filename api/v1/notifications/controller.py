from .serializer import NotificationListSerializer
from rest_framework import generics
from modules.booking.models import Notification
from api.v1.response_handler import response_handler, serialiser_errors
from django.utils.translation import ugettext_lazy as _

class NotificationListView(generics.ListAPIView):
	queryset = Notification.objects.all()
	serializer_class = NotificationListSerializer
	def list(self, request):
		queryset = self.get_queryset().filter(receiver=request.user)
		serializer = self.serializer_class(queryset, many=True)
		message = "Notification list fetched"
		return response_handler(message=message, data=serializer.data)	

class NotificationDeleteAPIView(generics.DestroyAPIView):
	queryset = Notification.objects.all()
	serializer_class = NotificationListSerializer
	def delete(self, request, pk):
		query_obj = self.get_object()
		query_obj.delete()
		message = _('Notification  deleted successfully')
		return response_handler(message=message)