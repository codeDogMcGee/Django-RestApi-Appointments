from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('appointments/', views.appointments_list, name='appointments'),
]