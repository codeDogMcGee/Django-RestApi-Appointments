from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.contrib.auth.models import User
from api.models import Appointment, Customer, Employee
from api.serializers import AppointmentSerializer, UserSerializer, \
    EmployeeSerializer, EmployeeAdminSerializer, CustomerSerializer, CustomerAdminSerializer
from api.permissions import IsAdminOrReadOnly


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class CustomerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Customer.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return CustomerAdminSerializer
        else:
            return CustomerSerializer

    def perform_create(self, serializer):
        serializer.save()


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Employee.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return EmployeeAdminSerializer
        else:
            return EmployeeSerializer

    def perform_create(self, serializer):
        serializer.save()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'appointments': reverse('appointment-list', request=request, format=format),
        'employees': reverse('employee-list', request=request, format=format),
        'customers': reverse('customer-list', request=request, format=format)
    }, permission_classes=[permissions.IsAdminUser])
