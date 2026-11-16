
from django.contrib import admin
from django.urls import path

from payroll import views as payroll_views
from employees import views as employee_views


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", payroll_views.home, name="home"),

    path(
        "payroll-dashboard/",
        payroll_views.payroll_dashboard,
        name="payroll_dashboard",
    ),

    path(
        "employees/",
        employee_views.employee_list,
        name="employee_list",
    ),
]
