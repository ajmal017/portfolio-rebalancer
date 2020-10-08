from rest_framework import serializers
from modules.configurations.models import *
from modules.teacher.models import Teacher, TeacherExperience, TeacherDocument
from modules.payment.models import PaymentDue
from users.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
import pdb
import re

class TeacherMusicGenreSerializer(serializers.ModelSerializer):
	class Meta:
		model = MusicGenre
		fields = ('id', 'name')

class InstrumentsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Instrument
		fields = ('id', 'name')

class TeacherExperienceSerializer(serializers.ModelSerializer):
	instruments_name = serializers.SerializerMethodField()
	class Meta:
		model = TeacherExperience
		fields = ('id', 'instruments_name', 'experience')
	def get_instruments_name(self, obj):
		return obj.instruments.name
 
class TeacherRegistrationSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'profile_image', 'username', 'email', 'password', 'dob', 'phone_number', 'role')
	def validate(self, validated_data):
		if User.objects.filter(email__iexact=validated_data.get('email')).exists():
			raise serializers.ValidationError("Email address aready exists !!")
		password = validated_data.get('password')
		confirm_password = self.context.get('request').data.get('confirm_password')
		if password != confirm_password:
			raise serializers.ValidationError("Password and Confirm password should be same.")
		return validated_data

	def create(self, validated_data):
		validated_data['password'] = make_password(validated_data['password'])
		instance = super(TeacherRegistrationSerializer, self).create(validated_data)
		Teacher.objects.create(user=instance)
		return instance

class TeacherDocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = TeacherDocument
		fields = '__all__'
class TeacherProfileSerializer(serializers.ModelSerializer):
	auth_token = serializers.SerializerMethodField()
	profile_image = serializers.SerializerMethodField()
	username = serializers.SerializerMethodField()
	email = serializers.SerializerMethodField()
	dob = serializers.SerializerMethodField()
	phone_number = serializers.SerializerMethodField()
	role = serializers.SerializerMethodField()
	country = serializers.SerializerMethodField()
	language = serializers.SerializerMethodField()
	music_genres = serializers.SerializerMethodField()
	instrument_experience = serializers.SerializerMethodField()
	time_zone = serializers.SerializerMethodField()
	documents =  serializers.SerializerMethodField()
	# time_zone = serializers.SerializerMethodField()
	class Meta:
		model = Teacher
		fields = '__all__'
	def get_auth_token(self, obj):
		token, created = Token.objects.get_or_create(user=obj.user)
		return token.key
	def get_profile_image(self, obj):
		return obj.user.profile_image.url

	def get_username(self, obj):
		return obj.user.username

	def get_email(self, obj):
		return obj.user.email

	def get_dob(self, obj):
		return obj.user.dob

	def get_phone_number(self, obj):
		return obj.user.phone_number

	def get_role(self, obj):
		return obj.user.role

	def get_language(self, obj):
		return obj.user.language

	def get_country(self, obj):
		return obj.user.country.name

	def get_time_zone(self, obj):
		return obj.user.time_zone

	def get_music_genres(self, obj):
		return TeacherMusicGenreSerializer(obj.music_genres.all(), many=True).data

	def get_instrument_experience(self, obj):
		return TeacherExperienceSerializer(obj.user.teacherexperience_set.all(), many=True).data

	def get_documents(self, obj):
		teacher_document = TeacherDocument.objects.filter(teacher=obj.user)
		return TeacherDocumentSerializer(teacher_document, many=True).data
	# def get_time_zone(self, obj):
	# 	return obj.user.time_zone

class TeacherProfileUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Teacher
		fields = ('gender', 'level', 'experience', 'video_file', 'short_introduction', 'about', 'price_per_lesson')
	def validate(self, attrs):
		# if not self.context.get('request').data.get('profile_image'):
		# 	raise serializers.ValidationError("Profile image is required")

		if not self.context.get('request').data.get('username'):
			raise serializers.ValidationError("username is required")

		if not self.context.get('request').data.get('dob'):
			raise serializers.ValidationError("DOB is required")

		if not self.context.get('request').data.get('phone_number'):
			raise serializers.ValidationError("Phone number is required")

		if not self.context.get('request').data.get('language'):
			raise serializers.ValidationError("Language is required")

		if not self.context.get('request').data.get('country'):
			raise serializers.ValidationError("Country is required")

		if not self.context.get('request').data.get('time_zone'):
			raise serializers.ValidationError("Time zone is required")

		return attrs

	def update(self, instance, validated_data):
		# teacher_information = {k.split('teacher[')[1].split(']')[0]: v for k, v in self.context.get('request').data.items() if re.search('teacher\[', k)}
		data = self.context.get('request').data
		if data.get('username') or data.get('dob') or data.get('phone_number') or data.get('language') or data.get('country') or data.get('time_zone'):
			teacher_information = dict()
			# teacher_information['profile_image'] = data.get('profile_image')
			teacher_information['username'] = data.get('username')
			teacher_information['dob'] = data.get('dob')
			teacher_information['phone_number'] = data.get('phone_number')
			teacher_information['language'] = data.get('language')
			teacher_information['country'] = data.get('country')
			teacher_information['time_zone'] = data.get('time_zone')
			User.objects.filter(id=instance.user.id).update(**teacher_information)
		if data.get('music_genres'):
			music_genres = [int(music_genre.get('id')) for music_genre in data.get('music_genres')]
			for music_genre in music_genres:
				instance.music_genres.add(music_genre)
		if data.get('instruments'):
			teacher_instruments = data.get('instruments')
			for teacher_instrument in teacher_instruments:
				instrument = Instrument.objects.get(name__iexact=teacher_instrument['instruments'])
				TeacherExperience.objects.update_or_create(teacher=instance.user, instruments=instrument, experience=teacher_instrument['experience'])

		return super(TeacherProfileUpdateSerializer, self).update(instance, validated_data)

class TeacherPaymentHistorySerializer(serializers.ModelSerializer):
	receiver_name = serializers.SerializerMethodField()
	amount = serializers.SerializerMethodField()
	created_at = serializers.DateTimeField(format="%d-%m-%Y")
	class Meta:
		model = PaymentDue
		fields = ('receiver_name', 'created_at', 'amount')
	def get_receiver_name(self, obj):
		return obj.booking.student.username	
	def get_amount(self, obj):
		return obj.booking.price + obj.booking.admin_commission