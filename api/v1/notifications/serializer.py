from rest_framework import serializers
from modules.booking.models import Notification
from datetime import datetime, timedelta
from django.utils.timezone import localtime

class NotificationListSerializer(serializers.ModelSerializer):
	sender = serializers.SerializerMethodField()
	created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S %p")
	class Meta:
		model = Notification
		fields = ('id', 'sender','title', 'note', 'created_at')
	# def get_sender(self, obj):
	# 	return "Puneet"
	def get_sender(self, obj):
		return obj.sender.username
