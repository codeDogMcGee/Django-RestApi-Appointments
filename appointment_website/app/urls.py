from django.urls import path
from django.conf.urls import url
from django.http import HttpResponseRedirect
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('appointments/', views.appointments_list, name='appointments'),
    path('make-appointment/', views.make_appointment, name='make-appointment'),
]