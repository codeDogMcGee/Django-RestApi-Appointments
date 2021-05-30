from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from api import views

# register ViewSets with the router
router = DefaultRouter()
router.register(r'past-appointments', views.PastAppointmentViewSet)
router.register(r'users', views.UserViewSet)

# include other views
urlpatterns = [
    path('', include(router.urls)),
    path('appointments/', views.AppointmentList.as_view(), name='appointment-list'),
    path('appointment-detail/<int:pk>/', views.AppointmentDetail.as_view(), name='appointment-detail'),
]

# include auth views
urlpatterns += [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'), # provides post endpoint to receive api tokens
]