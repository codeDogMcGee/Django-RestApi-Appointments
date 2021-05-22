from django.urls import path, include
from rest_framework.routers import DefaultRouter
from appointments import views
from rest_framework.urlpatterns import format_suffix_patterns

router = DefaultRouter()
router.register(r'appointments', views.AppointmentViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]

# from django.urls import path, include
# from appointments import views
# from appointments.views import AppointmentViewSet, UserViewSet, api_root
# from rest_framework import renderers
# from rest_framework.urlpatterns import format_suffix_patterns
#
# appointment_list = AppointmentViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# appointment_detail = AppointmentViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
# appointment_highlight = AppointmentViewSet.as_view({'get': 'highlight'},
#                                                    renderer_classes=[renderers.StaticHTMLRenderer])
#
# user_list = UserViewSet.as_view({
#     'get': 'list'
# })
#
# user_detail = UserViewSet.as_view({
#     'get': 'retrieve'
# })
#
# urlpatterns = [
#     path('', views.api_root),
#
#     path('appointments/', appointment_list, name='appointment-list'),
#     path('appointments/<int:pk>/', appointment_detail, name='appointment-detail'),
#     path('appointments/<int:pk>/highlight/', appointment_highlight, name='appointment-highlight'),
#
#     path('users/', user_list, name='user-list'),
#     path('users/<int:pk>/', user_detail, name='user-detail'),
#
# ]

# urlpatterns = [
#     path('', views.api_root),
#
#     path('appointments/', views.AppointmentsList.as_view(), name='appointment-list'),
#     path('appointments/<int:pk>/', views.AppointmentDetail.as_view(), name='appointment-detail'),
#     path('appointments/<int:pk>/highlight/', views.AppointmentHighlight.as_view(), name='appointment-highlight'),
#
#     path('users/', views.UserList.as_view(), name='user-list'),
#     path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
#
# ]

# we can use format_suffix_patterns to give us the
# future ability to use urls like
# http://example.com/api/items/4.json
# to specify json format, for example
# urlpatterns = format_suffix_patterns(urlpatterns)


# include login and logout views
urlpatterns += [
    path('api-auth', include('rest_framework.urls')),
]
