from rest_framework import serializers
from users.models import User
from modules.teacher.models import Teacher, TeacherDocument
from django.contrib.auth.hashers import make_password
from modules.configurations.models import Setting, Instrument, StaticPages, MusicGenre, Ratings
from modules.enquiry.models import Enquiry
from modules.booking.models import Media, Booking
from django.utils.translation import ugettext_lazy as _
from modules.chat.models import ChatRoom, ChatMessage
from django.utils.timezone import localtime
from api.v1.teachers.serializer import TeacherExperienceSerializer
import pdb
# class StudentRegistrationSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = User
# 		fields = ('id', 'profile_image', 'username', 'email', 'password', 'dob', 'phone_number', 'role')

# 	def validate(self, validated_data):
# 		if User.objects.filter(email__iexact=validated_data.get('email')).exists():
# 			raise serializers.ValidationError("Email address aready exists !!")
# 		password = validated_data.get('password')
# 		confirm_password = self.context.get('request').data.get('confirm_password')
# 		if password != confirm_password:
# 			raise serializers.ValidationError("Password and Confirm password should be same.")
# 		return validated_data

# 	def create(self, validated_data):
# 		validated_data['password'] = make_password(validated_data['password'])
# 		return super(StudentRegistrationSerializer, self).create(validated_data)



# class TeacherRegistrationSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = User
# 		fields = ('id', 'profile_image', 'username', 'email', 'password', 'dob', 'phone_number', 'role')
# 	def validate(self, validated_data):
# 		if User.objects.filter(email__iexact=validated_data.get('email')).exists():
# 			raise serializers.ValidationError("Email address aready exists !!")
# 		password = validated_data.get('password')
# 		confirm_password = self.context.get('request').data.get('confirm_password')
# 		if password != confirm_password:
# 			raise serializers.ValidationError("Password and Confirm password should be same.")
# 		return validated_data

# 	def create(self, validated_data):
# 		validated_data['password'] = make_password(validated_data['password'])
# 		instance = super(TeacherRegistrationSerializer, self).create(validated_data)
# 		Teacher.objects.create(user=instance)
# 		return instance

class UserRegistrationSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'profile_image', 'username', 'password', 'dob', 'phone_number', 'role')

	def validate(self, validated_data):
		email = self.context.get('request').data.get('email')
		if User.objects.filter(email__iexact=email).exists():
			raise serializers.ValidationError(_("Email address already exists"))
		password = validated_data.get('password')
		confirm_password = self.context.get('request').data.get('confirm_password')
		if password != confirm_password:
			raise serializers.ValidationError(_("Password and Confirm password should be same"))
		return validated_data
	def create(self, validated_data):
		validated_data['password'] = make_password(validated_data['password'])
		validated_data.update({"email": self.context.get('request').data.get('email')})
		if validated_data['role'] == "TEACHER":
			instance = super(UserRegistrationSerializer, self).create(validated_data)
			Teacher.objects.create(user=instance)
			return instance
		else:
			return super(UserRegistrationSerializer, self).create(validated_data)
		


class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField(required=True)
	password = serializers.CharField(max_length=200, required=True)

	def validate(self, attrs):
		users = User.objects.filter(email__iexact=attrs.get('email'))
		if not users.exists():
			raise serializers.ValidationError("Email Address not found.")

		if users.exists():
			user = users.first()
			if not user.check_password(attrs.get('password')):
				raise serializers.ValidationError("Email or Password is wrong")
		return attrs

class IntrumentsListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Instrument
		fields = ("id", "name")
class MusicGenresListSerializer(serializers.ModelSerializer):
	class Meta:
		model = MusicGenre
		fields = ("id", "name")

class TeacherListSerializer(serializers.ModelSerializer):
	profile_image = serializers.SerializerMethodField()
	username = serializers.SerializerMethodField()
	country = serializers.SerializerMethodField()
	genres = serializers.SerializerMethodField()
	# city = serializers.SerializerMethodField()
	instruments = serializers.SerializerMethodField()
	experience = serializers.SerializerMethodField()
	short_introduction = serializers.SerializerMethodField()
	rating = serializers.SerializerMethodField()
	price = serializers.SerializerMethodField()
	language = serializers.SerializerMethodField()
	class Meta:
		model = Teacher
		fields = ('id', 'profile_image', 'username','rating',  'genres', 'instruments', 'country', 'experience', 'short_introduction', 'price', 'language')

	def get_profile_image(self, obj):
		return obj.user.profile_image.url

	def get_username(self, obj):
		return obj.user.username

	def get_country(self, obj):
		return obj.user.country.name

	# def get_city(self, obj):
	# 	return obj.city
	def get_genres(self, obj):
		return MusicGenresListSerializer(obj.music_genres.all(), many=True).data

	def get_instruments(self, obj):
		return TeacherExperienceSerializer(obj.user.teacherexperience_set.all(), many=True).data

	def get_experience(self, obj):
		return obj.experience

	def get_short_introduction(self, obj):
		return obj.short_introduction

	def get_rating(self, obj):
		return 2.3

	def get_language(self, obj):
		return obj.user.language

	def get_price(self, obj):
		admin_commission = Setting.objects.filter(configuration=Setting.ADMIN_COMMISSION)
		if admin_commission.exists():
			admin_commission = admin_commission.first()
			admin_commission = obj.price_per_lesson * admin_commission.amount/100
			return obj.price_per_lesson + admin_commission
		else:
			admin_commission = obj.price_per_lesson * 18/100
			return obj.price_per_lesson + admin_commission

class TeacherRatingReviewSerializer(serializers.ModelSerializer):
	student = serializers.SerializerMethodField()
	class Meta:
		model = Ratings
		fields = ('student', 'rating', 'created_at', 'comment')

	def get_student(self, obj):
		return obj.student.username

class TeacherDocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = TeacherDocument
		fields = '__all__'

class TeacherDetailSerializer(serializers.ModelSerializer):
	price = serializers.SerializerMethodField()
	country = serializers.SerializerMethodField()
	username = serializers.SerializerMethodField()
	instruments = serializers.SerializerMethodField()
	music_genres = serializers.SerializerMethodField()
	review = serializers.SerializerMethodField()
	documents =  serializers.SerializerMethodField()
	class Meta:
		model = Teacher
		exclude = ('price_per_lesson', 'user')

	def get_profile_image(self, obj):
		return obj.user.profile_image.url

	def get_username(self, obj):
		return obj.user.username

	def get_country(self, obj):
		return obj.user.country.name
	def get_price(self, obj):
		admin_commission = Setting.objects.filter(configuration=Setting.ADMIN_COMMISSION)
		if admin_commission.exists():
			admin_commission = admin_commission.first()
			admin_commission = obj.price_per_lesson * admin_commission.amount/100
			return obj.price_per_lesson + admin_commission
		else:
			admin_commission = obj.price_per_lesson * 18/100
			return obj.price_per_lesson + admin_commission
	def get_instruments(self, obj):
		return TeacherExperienceSerializer(obj.user.teacherexperience_set.all(), many=True).data
	def get_music_genres(self, obj):
		return MusicGenresListSerializer(obj.music_genres.all(), many=True).data
	def get_review(self, obj):
		return TeacherRatingReviewSerializer(obj.teacher_rating.filter(is_verified=True, given_by="STUDENT"), many=True).data
	def get_documents(self, obj):
		teacher_document = TeacherDocument.objects.filter(teacher=obj.user)
		return TeacherDocumentSerializer(teacher_document, many=True).data

class EnquiryCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Enquiry
		fields = '__all__'

class UserStaticPageSerializer(serializers.ModelSerializer):
	class Meta:
		model = StaticPages
		fields = '__all__'

class ShareMediaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Media
		fields = '__all__'

class RatingReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ratings
		fields = '__all__'

class MessageUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','role',)

class ChatMessageSerializer(serializers.ModelSerializer):
	message_on = serializers.SerializerMethodField()
	# message_flow = serializers.SerializerMethodField()
	is_send = serializers.SerializerMethodField()
	# sender_detail = serializers.SerializerMethodField()
	room = serializers.SerializerMethodField()

	class Meta:
		model = ChatMessage
		fields = ('id', 'room','message_type', 'is_send', 'message', 'media_url','message_on','seen',)

	def get_message_on(self, obj):
		return localtime(obj.message_at).strftime('%d-%m-%Y %H:%M %p')

	def get_is_send(self, obj):
		if self.context.get('request').user == obj.sender:
			return True
		else:
			return False
		# return MessageUserSerializer(obj.sender).data

	def get_room(self, obj):
		return obj.room_id.room_number

class ChatCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = ChatMessage
		fields = ('id', 'room_id', 'message', 'message_type', 'media_url') 

class ChatListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = '__all__'

