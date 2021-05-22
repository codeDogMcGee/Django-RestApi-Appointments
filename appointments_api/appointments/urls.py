from django.urls import path
from appointments import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('all', views.AppointmentsList.as_view()),
    path('<int:pk>', views.AppointmentDetail.as_view()),
]

# we can use format_suffix_patterns to give us the
# future ability to use urls like
# http://example.com/api/items/4.json
# to specify json format, for example
urlpatterns = format_suffix_patterns(urlpatterns)
