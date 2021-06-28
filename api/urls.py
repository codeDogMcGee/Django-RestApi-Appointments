from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from api import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('settings/', views.HelperSettingsView.as_view(), name='helper-settings'),
    path('groups/', views.GroupIdsView.as_view(), name='groups'),

    path('users/', views.UsersView.as_view(), name='users'),
    path('users/<str:group_name>/', views.UsersView.as_view(), name='users-groups'),

    path('user/self/', views.UserSelfView.as_view(), name="user-self"),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    
    path('appointments/', views.AppointmentList.as_view(), name='appointment-list'),
    path('appointments/<int:pk>/', views.AppointmentDetail.as_view(), name='appointment-detail'),

    path('appointments-user/<int:pk>/', views.AppointmentsForUserView.as_view(), name='appointment-user'),
    
    path('past-appointments/', views.PastAppointmentList.as_view(), name='past-appointment-list'),
    path('past-appointment/<int:pk>/', views.PastAppointmentDetail.as_view(), name='past-appointment-detail'),

    path('schedules/', views.ScheduleList.as_view(), name='schedules-list'),
    path('schedule/<int:pk>/', views.ScheduleDetail.as_view(), name='schedule-detail'),

    path('menu/', views.MenuList.as_view(), name='menu-list'),
    # path('menu/<int:pk>/', views.ScheduleDetail.as_view(), name='menu-detail'),

]

# include auth views
urlpatterns += [
    path('api-token-auth/', views.CustomObtainAuthToken.as_view(), name='api_token_auth'),
    # path('api-token-auth/', obtain_auth_token, name='api_token_auth'), # provides a default post endpoint to receive api tokens
    # path('', include('django.contrib.auth.urls')),  # provides registration urls
]