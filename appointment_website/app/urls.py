from django.urls import path
from django.conf.urls import url
from django.http import HttpResponseRedirect
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('appointments/', views.appointments_list, name='appointments'),
    path('make-appointment/', views.make_appointment, name='make-appointment'),
    path('create-user/', views.create_user, name='create-user'),
    path('modify-user/', views.modify_user, name='modify-user'),

    # path('api-auth', include('rest_framework.urls')),  # provides login/logout views
]