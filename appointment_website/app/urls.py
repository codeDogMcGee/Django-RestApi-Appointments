from django.urls import path
from django.conf.urls import include, url
from django.http import HttpResponseRedirect
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('appointments/', views.appointments_list, name='appointments'),
    path('make-appointment/', views.CreateAppointmentView.as_view(), name='make-appointment'),
    path('create-user/', views.create_user, name='create-user'),
    # path('modify-user/', views.modify_user, name='modify-user'),
    path('user-page/', views.UserPageView.as_view(), name='user-page'),

    path('', include('django.contrib.auth.urls')),  # provides registration urls
]