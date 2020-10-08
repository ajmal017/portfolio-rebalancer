from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from modules.payment.models import PaymentHistory
from users.models import User
from rest_framework.authtoken.models import Token


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


class StudentProfileSerializer(serializers.ModelSerializer):
	auth_token = serializers.SerializerMethodField()
	country = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = ('id', 'auth_token', 'username','profile_image', 'email', 'dob', 'language', 'country', 'time_zone', 'phone_number', 'role', 'is_active')

	def get_auth_token(self, obj):
		token, created = Token.objects.get_or_create(user=obj)
		return token.key

	def get_country(self, obj):
		return obj.country.name

class StudentProfileUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('profile_image', 'username', 'dob', 'language', 'country', 'time_zone', 'phone_number')

class StudentPaymentHistorySerializer(serializers.ModelSerializer):
	receiver_name = serializers.SerializerMethodField()
	created_at = serializers.DateTimeField(format="%d-%m-%Y")
	class Meta:
		model = PaymentHistory
		fields = ('id', 'receiver_name', 'created_at', 'amount')
	def get_receiver_name(self, obj):
		return obj.booking.teacher.user.username