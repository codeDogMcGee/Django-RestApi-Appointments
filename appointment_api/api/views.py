from rest_framework import viewsets
from rest_framework import renderers
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view, action
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.contrib.auth.models import User
from api.models import Appointment, Customer, Employee
from api.serializers import AppointmentSerializer, UserSerializer, EmployeeSerializer, CustomerSerializer
from api.permissions import IsOwner


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'appointments': reverse('appointment-list', request=request, format=format),
        'employees': reverse('employee-list', request=request, format=format),
        'customers': reverse('customer-list', request=request, format=format)
    })
