from django.urls import path

from . import views

app_name = 'appointments'
urlpatterns = [
    path('', views.index, name='index'),
    path('make_appointment', views.make_appointment, name='make_appointment'),
    path('view_appointment/<int:appointment_id>', views.view_appointment, name='view_appointment'),
    path('view_appointments/<int:employee_id>', views.view_appointments_by_employee, name='view_appointment_by_employee'),
]
