from rest_framework import viewsets
from rest_framework import renderers
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view, action
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.contrib.auth.models import User
from appointments.models import Appointment
from appointments.serializers import AppointmentSerializer, UserSerializer
from appointments.permissions import IsOwnerOrReadOnly


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Additionally we also provide an extra `highlight` action.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # action decorator allows custom endpoints that aren't create, update, delete
    # include url_path as decorator argument to change the way the url is constructed
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        appointment = self.get_object()
        return Response(appointment.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'appointments': reverse('appointment-list', request=request, format=format)
    })






################################################################################
# Examples of some class based views
################################################################################
# from rest_framework.views import APIView
# from django.http import Http404
# from django.http import HttpResponse, JsonResponse
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.decorators import api_view
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
#
# class AppointmentHighlight(generics.GenericAPIView):
#     queryset = Appointment.objects.all()
#     renderer_classes = [renderers.StaticHTMLRenderer]
#
#     def get(self, request, *args, **kwargs):
#         appointment = self.get_object()
#         return Response(appointment.highlighted)
#
#
# class AppointmentsList(generics.ListCreateAPIView):
#     queryset = Appointment.objects.all()
#     serializer_class = AppointmentSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     # associate the appointment the the user that created it with owner=
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Appointment.objects.all()
#     serializer_class = AppointmentSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer



# class AppointmentsList(APIView):
#     def get(self, request, format=None):
#         appointments = Appointment.objects.all()
#         serializer = AppointmentSerializer(appointments, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = AppointmentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class AppointmentDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Appointment.objects.get(pk=pk)
#         except Appointment.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         appointment = self.get_object(pk)
#         serializer = AppointmentSerializer(appointment)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         appointment = self.get_object(pk)
#         serializer = AppointmentSerializer(appointment, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         appointment = self.get_object(pk)
#         appointment.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



################################################################################
# Examples of some function based views
################################################################################
# #usually dont let people post that are csrf_exempt, just use for debugging
# # @csrf_exempt
# @api_view(['GET', 'POST'])
# def appointment_list(request, format=None):
#     if request.method == 'GET':
#         appointments = Appointment.objects.all()
#         serializer = AppointmentSerializer(appointments, many=True)  # passing many=True gets all of them
#         # return JsonResponse(serializer.data, safe=False)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         # data = JSONParser().parse(request)
#         serializer = AppointmentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # return JsonResponse(serializer.data, status=201)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         # return JsonResponse(serializer.errors, status=400)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# # @csrf_exempt
# @api_view(['GET', 'PUT', 'DELETE'])
# def appointment_detail(request, pk, format=None):
#     try:
#         appointment = Appointment.objects.get(pk=pk)
#     except Appointment.DoesNotExist:
#         # return HttpResponse(status=404)
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = AppointmentSerializer(appointment)
#         # return JsonResponse(serializer.data)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         # data = JSONParser().parse(request)
#         serializer = AppointmentSerializer(appointment, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # return JsonResponse(serializer.data)
#             return Response(serializer.data)
#         # return JsonResponse(serializer.errors, status=400)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         appointment.delete()
#         # return HttpResponse(status=204)
#         return Response(status=status.HTTP_204_NO_CONTENT)