from django.urls import path ,include
from .controller import *

urlpatterns = [
  # path('sign-up',StudentRegistration.as_view()),
  path('<int:pk>/profile-update',StudentProfileUpdateAPIView.as_view()),
  path('<int:pk>/profile-picture-update',StudentProfilePictureUpdateAPIView.as_view()),
  path('booking/', include('api.v1.bookings.student_urls')),
  path('payment-history', PaymentHistorylistAPIView.as_view())
]