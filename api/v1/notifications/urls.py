from django.urls import path ,include
from .controller import *

urlpatterns = [ 
	path('list', NotificationListView.as_view()),
	path('delete/<int:pk>', NotificationDeleteAPIView.as_view())
]