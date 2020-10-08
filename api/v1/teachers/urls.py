from django.urls import path, include 
from .controller import *

urlpatterns=[
	# path('signup-initial',InitialRegistrationView.as_view()),
	path('<int:pk>/profile-update', TeacherProfileUpdateAPIView.as_view()),
	path('booking/',include('api.v1.bookings.teacher_urls')),
	path('payment-history', PaymentHistorylistAPIView.as_view()),
	path('<int:pk>/profile-picture-update',TeacherProfilePictureUpdateAPIView.as_view()),
	path('<int:pk>/document-update', TeacherDocumentDetailUpdateAPIView.as_view())
	# 5/
	# path('sign-up',TeacherRegistration.as_view()),
	
]