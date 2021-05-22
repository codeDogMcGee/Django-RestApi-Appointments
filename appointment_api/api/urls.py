from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r'appointments', views.AppointmentViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'customers', views.CustomerViewSet)

urlpatterns = [
    path('', include(router.urls))
]

# include login and logout views
urlpatterns += [
    path('api-auth', include('rest_framework.urls')),
]