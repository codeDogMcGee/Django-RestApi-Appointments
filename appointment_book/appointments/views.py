from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import Http404, HttpResponse

from .models import Appointment, Employee


def index(request):
    next_five_appointments = Appointment.objects.order_by('-appointment_datetime')[:5]
    context = {
        'next_five_appointments': next_five_appointments
    }
    return render(request, 'appointments/index.html', context)


def make_appointment(request):
    employees = Employee.objects.order_by('-first_name')
    context = {
        'employees': employees
    }
    return render(request, 'appointments/make_appointment.html', context)


def view_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    return render(request, 'appointments/view_appointment.html', {'appointment': appointment})


def view_appointments_by_employee(request, employee_id):
    return HttpResponse(f'These are appointments for {employee_id}')
