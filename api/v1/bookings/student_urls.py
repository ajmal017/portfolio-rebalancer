from django.urls import path ,include
from .student_controller import *

urlpatterns = [
  path('create',BookingCreateAPIView.as_view()),
  path('list', BookingView.as_view()),
  path('media-list', MediaListAPIView.as_view())
]