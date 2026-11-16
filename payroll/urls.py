
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="payroll_home"),
    path("dashboard/", views.payroll_dashboard, name="payroll_dashboard"),
]
