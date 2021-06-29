from django.core.exceptions import ValidationError
from django.http.response import Http404
from django.shortcuts import render
from django.views import View
from django.db.models import Q

from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken

from api.models import Appointment, EmployeeScheduleModel, GroupIdsModel, PastAppointment, HelperSettingsModel, ApiUser, ServiceMenuModel
from api import serializers
from api.utils.get_or_create_groups import get_or_create_groups
from api.utils.manage_appointments import execute_helper_functions
from api.validators import is_valid_group


class IndexView(View):
    template_name = 'api/index.html'
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return render(request, self.template_name)


class UserSelfView(APIView):
    """
    Get user object with self
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        serializer = serializers.AppUserWithGroupsSerializer(request.user)

        return Response(serializer.data)

class AppointmentList(APIView):
    """
    Read all appointments, or create new appointment
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        execute_helper_functions()
        if request.user.is_staff: # permissions.IsAdminUser
            appointments = Appointment.objects.all()
            serializer = serializers.AppointmentSerializer(appointments, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'Unauthorized to view this page.'})

    def post(self, request):
        serializer = serializers.AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(request.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDetail(APIView):
    """
    Read, Update, Delete functionality for one Appointment

    Customers and Employees should only be able to see their own appointments
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
        serializer = serializers.AppointmentSerializer(appointment)
        return Response(serializer.data)

    def put(self, request, pk):
        appointment = self._get_appointment(pk)
        serializer = serializers.AppointmentSerializer(appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        appointment = self._get_appointment(pk)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AppointmentsForUserView(APIView):
    """
    Read all appointments for a specific employee_id
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        execute_helper_functions()

        appointments = Appointment.objects.filter(Q(employee_id=pk) | Q(customer_id=pk))
        serializer = serializers.AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)


class PastAppointmentList(APIView):
    """
    Read all appointments
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        execute_helper_functions()

        appointments = PastAppointment.objects.all()
        serializer = serializers.PastAppointmentSerializer(appointments, many=True)
        return Response(serializer.data)


class PastAppointmentDetail(APIView):
    """
    Read only functionality for one Appointment
    """
    permission_classes = [permissions.IsAdminUser]

    def _get_appointment(self, pk):
        try:
            return PastAppointment.objects.get(pk=pk)
        except PastAppointment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        execute_helper_functions()

        appointment = self._get_appointment(pk)
        serializer = serializers.PastAppointmentSerializer(appointment)
        return Response(serializer.data)


class UsersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, group_name=''):

        if len(group_name) > 0:
                
            try:
                is_valid_group.validate(group_name)
            except ValidationError:#is_valid_group.validate(group_name)
                return Response({'error': f"[{group_name}] is not a valid group."})

            group_name = group_name.lower()
            group_name = group_name[0].upper() + group_name[1:]

            request_user_groups = []
            request_groups_query_set = request.user.groups.all()
            for group in request_groups_query_set:
                request_user_groups.append(group.name)

            users = None
            if (group_name == 'Customers' and 'Customers' in request_user_groups) or \
                (group_name == 'Employees' and 'Employees' in request_user_groups):
                # if it's a customer requesting customers only give them themselves
                users = [{'id': request.user.id, 'name': request.user.name, 'phone': request.user.phone}]
                serializer = serializers.AppUserSerializer(users, many=True)

            elif (group_name == 'Customers' and 'Employees' in request_user_groups) or (request.user.is_staff):
                # if an employee is requesting customers return them all active customers
                users = ApiUser.objects.filter(is_active=True).filter(groups__name=group_name)
                serializer = serializers.AppUserSerializer(users, many=True)

            elif group_name == 'Employees' and 'Customers' in request_user_groups:
                # if a customer is requesting employees don't include the phone numbers
                users = ApiUser.objects.filter(is_active=True).filter(groups__name=group_name)
                serializer = serializers.AppUserNoPhoneSerializer(users, many=True)

        elif request.user.is_staff:
            # admins can view all users
            users = ApiUser.objects.filter(is_active=True)
            serializer = serializers.AppUserWithGroupsSerializer(users, many=True)
    
        else:
            return Response('Unauthorized to view this page.')

        return Response(serializer.data)
    

    def post(self, request, group_name=''):
        
        if request.user.is_staff: #permissions.IsAdminUser
            if group_name != '':
                groups_dict = get_or_create_groups()

                serializer = serializers.AppCreateUserSerializer(data=request.data)
                if serializer.is_valid():

                    # make sure a valid group name was passed to the url
                    try:
                        group_name = is_valid_group.validate(group_name)
                    except ValidationError:
                        return Response({'Invalid Group Error': f"[{group_name}] is not a valid group."}, status=status.HTTP_400_BAD_REQUEST)

                    # create new user object
                    new_user = ApiUser.objects.create_user(
                        phone = serializer.data['phone'], 
                        name = serializer.data['name'], 
                        password = serializer.data['password_submitted']
                    )

                    # add the new user to the appropriate group
                    group = groups_dict[group_name]
                    group.user_set.add(new_user)

                    # set up employee schedule

                    return Response(request.data, status=status.HTTP_201_CREATED)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
            else:
                return Response({'error': 'Can only post to /users/<str:group_name>/'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Only admin users can create a new user.'}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # permissions are handled in _get_user()

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
            serializer = serializers.AppUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

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
                serializer = serializers.AppCreateUserSerializer(user, data=request.data)
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

    # def delete(self, request, pk):
        # TODO: to delete a user set up delete route 
        #       that doesn't delete but deactivates the user
        #       If it's an employee then make sure to also delete
        #       their schedule
    def delete(self, request, pk):
        user, error = self._get_user(pk, request.user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HelperSettingsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        helpers = HelperSettingsModel.objects.all()
        serializer = serializers.HelperSettingsSerializer(helpers, many=True)
        return Response(serializer.data)


class GroupIdsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        groups = GroupIdsModel.objects.all()
        serializer = serializers.GroupIdsSerializer(groups, many=True)
        return Response(serializer.data)

        
class CustomObtainAuthToken(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = serializers.AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        else:
            return Response(serializer.errors)


class ScheduleList(APIView):
    """
    Read all appointments, or create new appointment
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        schedules = EmployeeScheduleModel.objects.all()
        serializer = serializers.EmployeeScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

    # only admins and managers can post
    def post(self, request):
        request_user_groups = request.user.groups.all()

        if len(request_user_groups) == 1:
            request_user_group = request_user_groups[0]

            if request_user_group.name in ['Admins', 'Managers']:
                serializer = serializers.EmployeeScheduleSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else: 
                return Response('User not authorized to post a new schedule.')
        else:
            raise Exception(f"User is not a member of exactly one group. {list(request_user_groups)}")


class ScheduleDetail(APIView):
    """
    Read, Update, Delete functionality for one Appointment

    Customers and Employees should only be able to see their own appointments
    """
    permission_classes = [permissions.IsAuthenticated]

    # TODO: only let people change (PUT or DELETE) their own schedules, or admin, or manager

    def _get_schedule(self, pk):
        try:
            return EmployeeScheduleModel.objects.get(pk=pk)
        except EmployeeScheduleModel.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        schedule = self._get_schedule(pk)
        serializer = serializers.EmployeeScheduleSerializer(schedule)
        return Response(serializer.data)

    def put(self, request, pk):
        schedule = self._get_schedule(pk)
        serializer = serializers.EmployeeScheduleSerializer(schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        schedule = self._get_schedule(pk)
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MenuList(APIView):
    """
    Read all service items, or create new item
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        schedules = ServiceMenuModel.objects.all()
        serializer = serializers.ServiceMenuSerializer(schedules, many=True)
        return Response(serializer.data)

    # only admins and managers can post
    def post(self, request):
        request_user_groups = request.user.groups.all()

        if len(request_user_groups) == 1:
            request_user_group = request_user_groups[0]

            if request_user_group.name in ['Admins', 'Managers']:
                serializer = serializers.ServiceMenuSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else: 
                return Response('User not authorized to add menu item.')
        else:
            raise Exception(f"User is not a member of exactly one group. {list(request_user_groups)}")


# class ScheduleDetail(APIView):
#     """
#     Read, Update, Delete functionality for one Appointment

#     Customers and Employees should only be able to see their own appointments
#     """
#     permission_classes = [permissions.IsAuthenticated]

#     # TODO: only let people change (PUT or DELETE) their own schedules, or admin, or manager

#     def _get_schedule(self, pk):
#         try:
#             return EmployeeScheduleModel.objects.get(pk=pk)
#         except EmployeeScheduleModel.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         schedule = self._get_schedule(pk)
#         serializer = serializers.EmployeeScheduleSerializer(schedule)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         schedule = self._get_schedule(pk)
#         serializer = serializers.EmployeeScheduleSerializer(schedule, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         schedule = self._get_schedule(pk)
#         schedule.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)