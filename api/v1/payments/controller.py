from rest_framework import generics
from api.v1.response_handler import response_handler, serialiser_errors
from users.models import User
from django.db.models import Q
from .serializer import MakePaymentSerializer
from django.utils.translation import ugettext_lazy as _
from modules.booking.models import Booking
from modules.payment.models import PaymentHistory
from modules.configurations.tasks import payment_success_notify
import stripe
import pdb
stripe.api_key = "sk_test_51HOdhaJ8es8cba3riLQ44oiV6DRncvQx5NXEDei0PLG9B3264APKwnIVcj3Ops3tqeGTJpM88nBcHy7JsKLppdcC00zpsta4i2"

# token = stripe.Token.create(
#   card={
#     "number": "4242424242424242",
#     "exp_month": 9,
#     "exp_year": 2021,
#     "cvc": "314",
#   },
# )
# print("Token ", token.id)

class MakePaymentAPIView(generics.GenericAPIView):
	def post(self, request):
		serializer = MakePaymentSerializer(data=request.data)
		if serializer.is_valid():
			try:
				customers = stripe.Customer.list()
				existing_customer = next((customer for customer in customers if customer["email"] == serializer.data['email']), None)
				if not existing_customer:
					existing_customer = stripe.Customer.create(
						name = serializer.data['name'],
						email = serializer.data['email'],
						source= serializer.data['token'],
						address=serializer.data['address'],
						description=serializer.data['description'],
					  
					)
				# Creating the Charge Object with details of Charge
				amount = request.data.get('amount')
				if type(amount) == float:
					amount = amount * 100
					amount = int(amount)
				charge_service = stripe.Charge.create(
				amount= amount,
				currency="USD",
				receipt_email=serializer.data['email'],
				customer=existing_customer.id,
				description=serializer.data['description'],
				)
				# print(charge_service)
				if type(amount) == float:
					amount = amount / 100
					amount = int(amount)
				try:
					booking = Booking.objects.get(id=request.data.get('booking'))
					booking.payment_status = "SUCCESS"
					booking.save()
					payment_success_notify.delay(booking.id, amount)
					PaymentHistory.objects.create(booking=booking, status="Complete", transaction_id=charge_service.id, amount=amount)
				except Exception as ex:
					print(ex)
				print(existing_customer.id)
				message = "Payment completed successfully"
				return response_handler(message=message, data={})
			except Exception as ex:
				error_message = str(ex)
				message = _('Transaction failed, Please check error message')
				return response_handler(message=message, error_message=error_message, code=500)

		else:
			error_message = serialiser_errors(serializer)
			message = _('Transaction failed, Please check error message')
			return response_handler(message=message, error_message=error_message, code=500)
