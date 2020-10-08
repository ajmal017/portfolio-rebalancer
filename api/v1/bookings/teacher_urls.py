from django.urls import path ,include
from .teacher_controller import *

urlpatterns = [
  path('list', BookingView.as_view()),
  path('<int:pk>', UpdateBookingStatusView.as_view()),
  path('media-list', MediaListAPIView.as_view())
]