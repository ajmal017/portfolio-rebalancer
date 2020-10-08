from rest_framework import serializers
from modules.booking.models import Booking, Media
from modules.configurations.models import Setting

class BookingCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = '__all__'

class TeacherBookingListSerializers(serializers.ModelSerializer):
	created_at = serializers.DateTimeField(format="%d/%m/%Y")
	student_id = serializers.SerializerMethodField()
	student_profile = serializers.SerializerMethodField()
	student_name = serializers.SerializerMethodField()
	class Meta:
		model = Booking
		fields = ('id', 'student_profile', 'student_id', 'student_name', 'booking_status', 'payment_status', 'student_satisfy', 'teacher_satisfy', 'language', 'message', 'created_at', 'booking_message')
	def get_student_id(self, obj):
		return obj.student.id
	def get_student_profile(self, obj):
		return obj.student.profile_image.url
	def get_student_name(self, obj):
		return obj.student.username
class MediaListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Media
		fields = '__all__'
class TeacherShareVideoMediaListSerializer(serializers.ModelSerializer):
	booking = serializers.SerializerMethodField()
	class Meta:
		model = Media
		fields = '__all__'
	def get_booking(self, obj):
		return obj.booking.student.username

class StudentShareVideoMediaListSerializer(serializers.ModelSerializer):
	booking = serializers.SerializerMethodField()
	class Meta:
		model = Media
		fields = '__all__'
	def get_booking(self, obj):
		return obj.booking.teacher.user.username
# class ReceivedVideoMediaListSerializer(serializers.ModelSerializer):
# 	booking = serializers.SerializerMethodField()
# 	class Meta:
# 		model = Media
# 		fields = '__all__'
# 	def get_booking(self, obj):
# 		return obj.booking.student.username
class StudentBookingListSerializers(serializers.ModelSerializer):
	created_at = serializers.DateTimeField(format="%d/%m/%Y")
	teacher_profile = serializers.SerializerMethodField()
	teacher_id =  serializers.SerializerMethodField()
	teacher_name = serializers.SerializerMethodField()
	price = serializers.SerializerMethodField()
	class Meta:
		model = Booking
		fields = ('id', 'teacher_profile', 'teacher_id', 'teacher_name', 'booking_status', 'payment_status', 'student_satisfy', 'teacher_satisfy',  'language', 'message', 'price', 'created_at')
	def get_teacher_id(self, obj):
		return obj.teacher.id
	def get_teacher_profile(self, obj):
		return obj.teacher.user.username
	def get_teacher_name(self, obj):
		return obj.teacher.user.username
	def get_price(self, obj):
		return obj.price + obj.admin_commission