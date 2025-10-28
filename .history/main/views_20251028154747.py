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

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment
from .forms import AppointmentForm

def manage_appointments(request):
    appointments = Appointment.objects.all().order_by('date', 'time')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_appointments')  # بعد الإضافة، نرجع نفس الصفحة
    else:
        form = AppointmentForm()

    return render(request, 'appointments_manage.html', {
        'appointments': appointments,
        'form': form
    })


def edit_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('manage_appointments')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'edit_appointment.html', {'form': form, 'appointment': appointment})


def delete_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    if request.method == 'POST':
        appointment.delete()
        return redirect('manage_appointments')
    return render(request, 'delete_confirm.html', {'appointment': appointment})
from django.http import JsonResponse
from .models import Appointment
from .forms import AppointmentForm

def appointments_ajax(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            # نرجع البيانات الجديدة للـ frontend
            return JsonResponse({
                "status": "success",
                "id": appointment.id,
                "name": appointment.name,
                "doctor": appointment.doctor.name,
                "specialty": appointment.doctor.specialty,
                "date": appointment.date.strftime("%Y-%m-%d"),
                "time": appointment.time.strftime("%H:%M"),
                "message": appointment.message,
            })
        else:
            return JsonResponse({"status": "error", "errors": form.errors})
    else:
        # GET → نرجع كل المواعيد
        appointments = Appointment.objects.all().order_by('date', 'time')
        data = []
        for app in appointments:
            data.append({
                "id": app.id,
                "name": app.name,
                "doctor": app.doctor.name,
                "specialty": app.doctor.specialty,
                "date": app.date.strftime("%Y-%m-%d"),
                "time": app.time.strftime("%H:%M"),
                "message": app.message,
            })
        return JsonResponse({"appointments": data})
