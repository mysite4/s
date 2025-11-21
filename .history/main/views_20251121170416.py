from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import Appointment, Patient, Notification, Invoice, AccountingItem, DoctorSchedule, Payment
from .forms import AppointmentForm, PatientForm

# الصفحة الرئيسية
def home(request):
    return render(request, 'home.html')


# صفحة الحجز
def booking_page(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()

            patient_name = form.cleaned_data['name']
            patient_phone = form.cleaned_data['phone']
            patient_notes = form.cleaned_data.get('message', '')

            patient, created = Patient.objects.update_or_create(
                name=patient_name,
                defaults={
                    'phone': patient_phone,
                    'notes': patient_notes
                }
            )

            return render(request, 'booking_success.html')
    else:
        form = AppointmentForm()
    return render(request, 'booking.html', {'form': form})


# عرض جميع المواعيد
def appointments(request):
    appointments_list = Appointment.objects.all().order_by('-date', '-time')
    return render(request, 'services/appointments.html', {'appointments': appointments_list})


# عرض وإضافة المرضى
def patients_view(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patients')
    else:
        form = PatientForm()

    patients_list = Patient.objects.all().order_by('-id')
    return render(request, 'services/patients.html', {'form': form, 'patients': patients_list})


# صفحة المحاسبة
def accounting_dashboard(request):
    invoices = Invoice.objects.all().order_by('-date')
    accounting_data = []

    for invoice in invoices:
        accounting_data.append({
            'invoice_number': invoice.number,
            'patient_name': invoice.appointment.name if invoice.appointment else "غير مرتبط",
            'total_amount': invoice.total_amount,
            'paid_amount': invoice.paid_amount,
            'remaining_amount': invoice.remaining_amount,
            'payments': invoice.payments.all()  # كل دفعة مرتبطة بالفاتورة
        })

    return render(request, 'services/accounting.html', {'accounting_data': accounting_data})


# صفحة الاستقبال
def reception(request):
    doctors = DoctorSchedule.objects.all()
    return render(request, 'services/reception.html', {'doctors': doctors})


# صفحة المهام
def tasks(request):
    return render(request, 'services/tasks.html')


# صفحة الطوارئ
def emergency(request):
    return render(request, 'services/emergency.html')


# تعديل موعد باستخدام AJAX
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


# صفحة الإحصائيات
def stats_view(request):
    today = timezone.localdate()

    total_patients = Patient.objects.count()
    visits_today = Appointment.objects.filter(created_at__date=today).count()

    context = {
        'total_patients': total_patients,
        'visits_today': visits_today,
    }
    return render(request, 'services/statistics.html', context)


# صفحة الإشعارات
def notifications_page(request):
    notifications = Notification.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'services/notifications.html', {'notifications': notifications})
