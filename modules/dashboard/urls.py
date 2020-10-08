from django.urls import path
from .views import *
urlpatterns = [
    
    path("dashboard_count", DashboardCountView.as_view()),
    path("dashboard_pie_chart", BookingPieChartCount.as_view()),
    path("dashboard_line_chart", BookingLineChartCount.as_view()),
    path("dashboard_bargraph", BookingGraphView.as_view())

]

