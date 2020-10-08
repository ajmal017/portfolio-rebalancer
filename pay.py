import stripe
stripe.api_key = "sk_test_51HOdhaJ8es8cba3riLQ44oiV6DRncvQx5NXEDei0PLG9B3264APKwnIVcj3Ops3tqeGTJpM88nBcHy7JsKLppdcC00zpsta4i2"
# stripe.api_key = "pk_test_51HOdhaJ8es8cba3r6x7tcXChnFrrqboLHFfMWty5zlRv6saXZzwBCFmaR1JdbFS576SGiA75xXr9A0DfltA5Z8tg009B1ZqJD8"
# stripe.Customer.create(
#   description="My First Test Customer (created for API docs)",
#   email="mohan@yopmail.com",
#   name="mohan",
#   phone="7737202975"
# )


# cus_I5MNEhbXXgEOVP
import stripe
# stripe.api_key = "sk_test_51HOdhaJ8es8cba3riLQ44oiV6DRncvQx5NXEDei0PLG9B3264APKwnIVcj3Ops3tqeGTJpM88nBcHy7JsKLppdcC00zpsta4i2"

account = stripe.Account.create(
  type="custom",
  country="US",
  email="jenny.rosen@example.com",
  capabilities={
    "card_payments": {"requested": True},
    "transfers": {"requested": True},
  },
)
print(account)


# customer = stripe.Customer.create(
#       description="My Stripe Customer Id",
#       email="pawan@yopmail.com",
#       name="Pawan",
#       phone="8696083984"
#       )            
# print(customer)
            # instance.stripe_customer_id=customer.id
            # instance.save()

# print(customer.id)
# print(customer)


# import stripe
# stripe.api_key = "sk_test_51HOdhaJ8es8cba3riLQ44oiV6DRncvQx5NXEDei0PLG9B3264APKwnIVcj3Ops3tqeGTJpM88nBcHy7JsKLppdcC00zpsta4i2"

# customers = stripe.Customer.list(limit=3)
# print(len(customers))
# print(customers)

# dicts = [
# { "name": "Tom", "age": 10 },
# { "name": "Mark", "age": 5 },
# { "name": "Pam", "age": 7 },
# { "name": "Dick", "age": 12 }
# ]

# z = next(item for item in dicts if item["name"] == "Pam")
# print(z)

# import stripe
# stripe.api_key = "sk_test_obfuscated_offline_key"

# payment_intent = stripe.PaymentIntent.create(
#   amount=999,
#   currency='usd',
#   description='Software development services',
# )
# print("Payment Intent", payment_intent)

# customer = stripe.Customer.create(
#   name='Sonu Jain',
#   email = "sonu@yopmail.com",
#   address={
#     'line1': '510 Townsend St',
#     'postal_code': '98140',
#     'city': 'San Francisco',
#     'state': 'CA',
#     'country': 'US',
#   },
# )
# print("Customer", customer)

###################################
# token = stripe.Token.create(
#   card={
#     "number": "4242424242424242",
#     "exp_month": 9,
#     "exp_year": 2021,
#     "cvc": "314",
#   },
# )
# print("Token ", token.id)



# charge_service = stripe.Charge.create(
# 	amount= amount * 100,
# 	currency="USD",
# 	receipt_email=email,
# 	customer=existing_customer.stripe_customer_id,
# 	description=description,
# 	)
# print(charge_service)


# token = token.id
# charge = stripe.Charge.create(
#   amount=200000,
#   currency='usd',
#   description='Example charge',
#   source=token,
# )
# print("Charge", charge)

# token = token.id
# tok_1HQ54KJ8es8cba3rR6lWWq3M

# token =  token # Using Flask
# print(token)
# charge = stripe.Charge.create(
#   amount=999,
#   currency='USD',
#   description='Example charge',
#   source=token,
# )
# print(charge)


# stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

# payment_intent = stripe.PaymentIntent.create(
#   amount=1099,
#   currency='usd',
#   description='Software development services',
# )
# print(payment_intent)

# customer = stripe.Customer.create(
#   name='Jenny Rosen',
#   address={
#     'line1': '510 Townsend St',
#     'postal_code': '98140',
#     'city': 'San Francisco',
#     'state': 'CA',
#     'country': 'US',
#   },
# )
# print(customer)


# countries = {'AF': 'Afghanistan', 'AX': 'Åland Islands', 'AL': 'Albania', 'DZ': 'Algeria', 'AS': 'American Samoa', 'AD': 'Andorra', 
# 'AO': 'Angola', 'AI': 'Anguilla', 'AQ': 'Antarctica', 'AG': 'Antigua and Barbuda', 'AR': 'Argentina', 'AM': 'Armenia',
# 'AW': 'Aruba', 'AU': 'Australia', 'AT': 'Austria', 'AZ': 'Azerbaijan', 'BS': 'Bahamas', 'BH': 'Bahrain', 'BD': 'Bangladesh',
# 'BB': 'Barbados', 'BY': 'Belarus'}

# new_dict = []
# i = 1
# for country in countries:
# 	print(i)
# 	# new_dict.update({'country_code': country, 'country_name': countries[country]})
# 	# new_dict[country] = countries[country]
# 	new_dict.append({'country_code': country, 'country_name': countries[country]})
# 	i+=1
# 	# print(country, '->', countries[country])
# print(new_dict)

# payment_intent = stripe.PaymentIntent.create(
#   payment_method_types=['card'],
#   amount=1000,
#   currency='usd',
#   on_behalf_of=''
# )
# print(payment_intent)

# transfer = stripe.Transfer.create(
#   amount=1000,
#   currency="usd",
#   source_transaction="{CHARGE_ID}",
#   destination="{{CONNECTED_STRIPE_ACCOUNT_ID}}",
# )
# print(transfer)