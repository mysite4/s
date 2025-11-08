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
from .models import Appointment

def appointments(request):
    # جلب جميع المواعيد من قاعدة البيانات
    appointments = Appointment.objects.all().order_by('-date', '-time')
    return render(request, 'services/appointments.html', {'appointments': appointments})
from django.shortcuts import render, redirect
from .models import Patient
from .forms import PatientForm

def patients_view(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()  # ✅ هنا يتم حفظ المريض فعليًا في قاعدة البيانات
            return redirect('patients')
    else:
        form = PatientForm()

    patients_list = Patient.objects.all().order_by('-id')
    return render(request, 'services/patients.html', {'form': form, 'patients': patients_list})

from django.http import JsonResponse

def edit_appointment(request):
    if request.method == "POST":
        appointment_id = request.POST.get("appointment_id")
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.name = request.POST.get("patient_name")
        appointment.date = request.POST.get("date")
        appointment.time = request.POST.get("time")
        appointment.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})
