from django.urls import path, include 
from .controller import *

urlpatterns=[
	path('pay',MakePaymentAPIView.as_view()),
	
	
]