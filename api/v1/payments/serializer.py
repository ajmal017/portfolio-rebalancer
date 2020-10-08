from rest_framework import serializers

class MakePaymentSerializer(serializers.Serializer):
	booking = serializers.IntegerField(required=True, error_messages={'required': 'Booking required'})
	name =  serializers.CharField(required=True, error_messages={'required': 'Name is required'})
	email = serializers.EmailField(required=True, error_messages={'required': 'Email is required'})
	token = serializers.CharField(required=True, error_messages={'required': 'Token is required'})
	address = serializers.DictField(required=True, error_messages={'required': 'Address is required'})
	description = serializers.CharField(required=True, error_messages={'required': 'Description is required'})
	# amount = serializers.IntegerField(required=True, error_messages={'required': 'Amount is required'})
