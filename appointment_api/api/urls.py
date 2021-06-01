from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from api import views

# register ViewSets with the router
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'helpers', views.HelpersViewSet)

# include other views
urlpatterns = [
    path('', include(router.urls)),
    path('appointments/', views.AppointmentList.as_view(), name='appointment-list'),
    path('appointment/<int:pk>/', views.AppointmentDetail.as_view(), name='appointment-detail'),
    path('past-appointments/', views.PastAppointmentList.as_view(), name='past-appointment-list'),
    path('past-appointment/<int:pk>/', views.PastAppointmentDetail.as_view(), name='past-appointment-detail'),
    path('appointments-employee/<int:pk>/', views.AppointmentsForEmployeeIdView.as_view(), name='appointments-employee'),
    path('appointments-customer/<int:pk>/', views.AppointmentsForCustomerIdView.as_view(), name='appointments-customer'),
]

# include auth views
urlpatterns += [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'), # provides post endpoint to receive api tokens
]