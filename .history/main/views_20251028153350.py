from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
from django.shortcuts import render

def booking_page(request):
    return render(request, 'booking.html')


def appointments(request):
    return render(request, 'services/appointments.html')

def patients(request):
    return render(request, 'services/patients.html')

def accounting(request):
    return render(request, 'services/accounting.html')

def reception(request):
    return render(request, 'services/reception.html')

def notifications(request):
    return render(request, 'services/notifications.html')

def statistics(request):
    return render(request, 'services/statistics.html')

def tasks(request):
    return render(request, 'services/tasks.html')

def emergency(request):
    return render(request, 'services/emergency.html')

from django.shortcuts import render, redirect
from .forms import AppointmentForm

def booking_page(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'booking_success.html')
    else:
        form = AppointmentForm()
    return render(request, 'booking.html', {'form': form})

from django.shortcuts import render
from django.http import JsonResponse
from .models import Appointment

def appointments_page(request):
    appointments = Appointment.objects.all()
    return render(request, 'services/appointments.html', {'appointments': appointments})

def appointments_ajax(request):
    if request.method == "POST" and request.is_ajax():
        patient_name = request.POST.get('patient_name')
        date = request.POST.get('date')
        time = request.POST.get('time')
        doctor_name = request.POST.get('doctor_name')

        appointment = Appointment.objects.create(
            patient_name=patient_name,
            date=date,
            time=time,
            doctor_name=doctor_name
        )
        return JsonResponse({
            'success': True,
            'appointment': {
                'id': appointment.id,
                'patient_name': appointment.patient_name,
                'date': appointment.date,
                'time': appointment.time,
                'doctor_name': appointment.doctor_name,
            }
        })
    return JsonResponse({'success': False})
