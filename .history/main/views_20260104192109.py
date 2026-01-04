from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from .models import Appointment, Patient, Notification, Invoice, Payment, AccountingItem, DoctorSchedule, Doctor
from .forms import AppointmentForm, PatientForm
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt

# ------------------- الصفحة الرئيسية -------------------
def home(request):
    return render(request, 'home.html')
def booking_page(request):
    doctors = Doctor.objects.all()
    if request.method == 'POST':
        patient_name = request.POST.get('name')
        patient_phone = request.POST.get('phone')
        patient_email = request.POST.get('email', '')
        patient_notes = request.POST.get('message', '')
        date = request.POST.get('date')
        time = request.POST.get('time')
        doctor_id = request.POST.get('doctor')

        if not all([patient_name, patient_phone, date, time, doctor_id]):
            return render(request, 'booking.html', {
                'doctors': doctors,
                'error': 'الرجاء ملء جميع الحقول'
            })

        # حفظ المريض
        patient, created = Patient.objects.update_or_create(
            name=patient_name,
            defaults={
                'phone': patient_phone,
                'email': patient_email,
                'notes': patient_notes
            }
        )

        # الحصول على الطبيب
        doctor = get_object_or_404(Doctor, id=doctor_id)

        # إنشاء الموعد
        appointment = Appointment.objects.create(
            name=patient_name,
            phone=patient_phone,
            date=date,
            time=time,
            doctor=doctor,
            message=patient_notes,
            service_price=500
        )

        # إنشاء الفاتورة
        paid_amount = float(request.POST.get('paid_amount', 0))
        invoice_number = "INV-" + get_random_string(6).upper()
        invoice = Invoice.objects.create(
            appointment=appointment,
            number=invoice_number,
            total_amount=500,
            paid_amount=paid_amount,
            date=timezone.now()
        )

        if paid_amount > 0:
            Payment.objects.create(
                invoice=invoice,
                amount=paid_amount,
                paid_at=timezone.now()
            )

        return render(request, 'booking_success.html', {'invoice': invoice})

    return render(request, 'booking.html', {'doctors': doctors})

# ------------------- عرض جميع المواعيد -------------------
def appointments(request):
    appointments_list = Appointment.objects.all().order_by('-date', '-time')
    return render(request, 'services/appointments.html', {'appointments': appointments_list})


# ------------------- عرض وإضافة المرضى -------------------
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


# ------------------- صفحة المحاسبة -------------------
def accounting_dashboard(request):
    items = AccountingItem.objects.all().order_by('date')
    invoices = Invoice.objects.all().order_by('-date')
    context = {
        'accounting_items': items,
        'invoices': invoices
    }
    return render(request, 'services/accounting.html', context)


# ------------------- صفحة الاستقبال -------------------
def reception(request):
    doctors = DoctorSchedule.objects.all()
    return render(request, 'services/reception.html', {'doctors': doctors})


# ------------------- صفحة المهام -------------------
def tasks(request):
    return render(request, 'services/tasks.html')


# ------------------- صفحة الطوارئ -------------------
def emergency(request):
    return render(request, 'services/emergency.html')


# ------------------- تعديل موعد باستخدام AJAX -------------------
def edit_appointment(request):
    if request.method == "POST":
        appointment_id = request.POST.get("appointment_id")
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.name = request.POST.get("patient_name")
        appointment.date = request.POST.get("date")
        appointment.time = request.POST.get("time")
        appointment.phone = request.POST.get("phone")

        appointment.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})


# ------------------- إضافة موعد جديد باستخدام AJAX -------------------
@csrf_exempt
def add_appointment(request):
    if request.method == "POST":
        patient_name = request.POST.get("patient_name")
        phone = request.POST.get("phone")  # ✅ مهم
        date = request.POST.get("date")
        time = request.POST.get("time")
        doctor_name = request.POST.get("doctor_name")

        if not all([patient_name, phone, date, time, doctor_name]):
            return JsonResponse({"success": False, "error": "البيانات غير مكتملة"})

        doctor, created = Doctor.objects.get_or_create(
            name=doctor_name,
            defaults={'specialty': 'عام'}
        )

        Appointment.objects.create(
            name=patient_name,
            phone=phone,          # ✅
            date=date,
            time=time,
            doctor=doctor
        )

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})

# ------------------- صفحة الإحصائيات -------------------
def stats_view(request):
    today = timezone.localdate()
    total_patients = Patient.objects.count()
    visits_today = Appointment.objects.filter(created_at__date=today).count()
    context = {
        'total_patients': total_patients,
        'visits_today': visits_today,
    }
    return render(request, 'services/statistics.html', context)


# ------------------- صفحة الإشعارات -------------------
def notifications_page(request):
    notifications = Notification.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'services/notifications.html', {'notifications': notifications})


# ------------------- طباعة الفاتورة -------------------
def print_invoice_view(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    payments = invoice.payments.all()

    context = {
        'invoice': invoice,
        'payments': payments,
    }
    return render(request, 'print_invoice.html', context)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Appointment

@csrf_exempt
def delete_appointment(request):
    if request.method == "POST":
        appointment_id = request.POST.get("appointment_id")

        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.delete()
            return JsonResponse({"success": True})
        except Appointment.DoesNotExist:
            return JsonResponse({"success": False})

    return JsonResponse({"success": False})

from django.shortcuts import render

def price_list(request):
    return render(request, 'services/price_list.html')

