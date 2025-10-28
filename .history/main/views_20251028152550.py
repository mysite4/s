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

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Appointment
from .forms import AppointmentForm

def appointments_view(request):
    """
    View متكاملة لإدارة المواعيد:
    - GET: عرض جميع المواعيد
    - POST: إضافة موعد جديد عبر Ajax
    - DELETE: حذف موعد عبر Ajax
    - PUT: تعديل موعد عبر Ajax
    """
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # إضافة موعد جديد
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            data = {
                'id': appointment.id,
                'patient_name': appointment.patient_name,
                'date': appointment.date.strftime('%Y-%m-%d'),
                'time': appointment.time.strftime('%H:%M'),
                'doctor_name': appointment.doctor_name,
            }
            return JsonResponse({'success': True, 'appointment': data})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    elif request.method == 'DELETE' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # حذف موعد
        import json
        body = json.loads(request.body)
        appointment_id = body.get('id')
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.delete()
        return JsonResponse({'success': True})

    elif request.method == 'PUT' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # تعديل موعد
        import json
        body = json.loads(request.body)
        appointment_id = body.get('id')
        appointment = get_object_or_404(Appointment, id=appointment_id)
        form = AppointmentForm(body, instance=appointment)
        if form.is_valid():
            appointment = form.save()
            data = {
                'id': appointment.id,
                'patient_name': appointment.patient_name,
                'date': appointment.date.strftime('%Y-%m-%d'),
                'time': appointment.time.strftime('%H:%M'),
                'doctor_name': appointment.doctor_name,
            }
            return JsonResponse({'success': True, 'appointment': data})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    # GET: عرض جميع المواعيد
    appointments = Appointment.objects.all()
    form = AppointmentForm()
    return render(request, 'services/appointments.html', {'appointments': appointments, 'form': form})
