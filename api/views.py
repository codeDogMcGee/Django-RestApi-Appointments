from django.core.exceptions import ValidationError
from django.http.response import Http404
from django.shortcuts import render
from django.views import View

from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView

from api.models import Appointment, PastAppointment, HelperSettingsModel, ApiUser
from api.serializers import AppointmentSerializer, HelperSettingsSerializer, AppUserSerializer, AppCreateUserSerializer, PastAppointmentSerializer
from api.utils.utils import get_or_create_groups
from api.utils.manage_appointments import execute_helper_functions
from api.validators import is_valid_group


class IndexView(View):
    template_name = 'api/index.html'
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return render(request, self.template_name)


class AppointmentList(APIView):
    """
    Read all appointments, or create new appointment
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        execute_helper_functions()

        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDetail(APIView):
    """
    Read, Update, Delete functionality for one Appointment
    """
    permission_classes = [permissions.IsAuthenticated]

    def _get_appointment(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        execute_helper_functions()

        appointment = self._get_appointment(pk)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    def put(self, request, pk):
        appointment = self._get_appointment(pk)
        serializer = AppointmentSerializer(appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        appointment = self._get_appointment(pk)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PastAppointmentList(APIView):
    """
    Read all appointments
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        execute_helper_functions()

        appointments = PastAppointment.objects.all()
        serializer = PastAppointmentSerializer(appointments, many=True)
        return Response(serializer.data)


class PastAppointmentDetail(APIView):
    """
    Read only functionality for one Appointment
    """
    permission_classes = [permissions.IsAuthenticated]

    def _get_appointment(self, pk):
        try:
            return PastAppointment.objects.get(pk=pk)
        except PastAppointment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        execute_helper_functions()

        appointment = self._get_appointment(pk)
        serializer = PastAppointmentSerializer(appointment)
        return Response(serializer.data)


class HelperSettingsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        helpers = HelperSettingsModel.objects.all()
        serializer = HelperSettingsSerializer(helpers, many=True)
        return Response(serializer.data)


class UsersView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, group_name=''):

        if group_name != '':
            try:
                users = ApiUser.objects.filter(groups__name=is_valid_group.validate(group_name))
            except ValidationError:
                return Response({'Invalid Group Error': f"[{group_name}] is not a valid group."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            users = ApiUser.objects.all()

        serializer = AppUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, group_name=''):
        
        if group_name != '':
            groups_dict = get_or_create_groups()

            serializer = AppCreateUserSerializer(data=request.data)
            if serializer.is_valid():

                try:
                    group_name = is_valid_group.validate(group_name)
                except ValidationError:
                    return Response({'Invalid Group Error': f"[{group_name}] is not a valid group."}, status=status.HTTP_400_BAD_REQUEST)

                new_user = ApiUser.objects.create_user(
                    phone = serializer.data['phone'], 
                    name = serializer.data['name'], 
                    password = serializer.data['password_submitted']
                )

                customer_group = groups_dict[group_name]
                customer_group.user_set.add(new_user)

                return Response(request.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        else:
            return Response({'Post request error': 'Can only post to /users/<str:group_name>/'}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    permission_classes = [permissions.AllowAny]  # permissions are handled in _get_user()

    def _get_user(self, pk, active_user):
        '''
        This method verifies that the logged in user is the same as
        the one being requested before returning the user object. Or that
        the logged in user is an administrator.
        '''
        error_object = {'error': ''}
        try:
            user = ApiUser.objects.get(pk=pk)            
            if user != active_user and active_user.is_staff is False:  # handle permissions
                user = None
                error_object = {'error': 'User is not allowed to view this page.'}
            return user, error_object
        except ApiUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user, err = self._get_user(pk, request.user)
        if err['error'] != '':
            return Response(err, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = AppUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        user, err = self._get_user(pk, request.user)
        if err['error'] != '':
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:    
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        '''
        A full user object must be passed:
        {
            "phone": "5555555555",
            "name": "Jesse",
            "password_submitted": "password1"   
        }
        '''

        if 'password_submitted' in request.data.keys():
            
            user, err = self._get_user(pk, request.user)
            if err['error'] != '':
                return Response(err, status=status.HTTP_403_FORBIDDEN)
            else:
                serializer = AppCreateUserSerializer(user, data=request.data)
                if serializer.is_valid():
                    serializer.save()

                    user, err = self._get_user(pk, request.user)
                    if err['error'] != '':
                        return Response(err, status=status.HTTP_403_FORBIDDEN)
                    else:
                        user.set_password(serializer.data['password_submitted'])
                        user.save()
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'Password not provided error': 'Must provide a password with a user update.'}, status=status.HTTP_400_BAD_REQUEST)


# class AppointmentsForEmployeeIdView(APIView):
#     """
#     Read all appointments for a specific employee_id
#     """
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, pk):
#         execute_helper_functions()

#         appointments = Appointment.objects.filter(employee_id=pk)
#         serializer = AppointmentSerializer(appointments, many=True)
#         return Response(serializer.data)


# class AppointmentsForCustomerIdView(APIView):
#     """
#     Read all appointments for a specific employee_id
#     """
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, pk):
#         execute_helper_functions()

#         appointments = Appointment.objects.filter(customer_id=pk)
#         serializer = AppointmentSerializer(appointments, many=True)
#         return Response(serializer.data)