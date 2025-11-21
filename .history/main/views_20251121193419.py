from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import Appointment, Patient, Notification, Invoice, Payment, AccountingItem, DoctorSchedule
from .forms import AppointmentForm, PatientForm

# الصفحة الرئيسية
def home(request):
    return render(request, 'home.html')


# صفحة الحجز مع إنشاء الفاتورة والدفع
def booking_page(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # حفظ الموعد
            appointment = form.save()

            # إنشاء أو تحديث المريض
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

            # إنشاء الفاتورة تلقائيًا بسعر الكشف
            invoice = Invoice.objects.create(
                appointment=appointment,
                total_amount=appointment.service_price,
                paid_amount=0  # سيتم إدخال الدفع لاحقًا
            )

            # التحقق من الدفع الفوري من الفورم (إضافة حقل مبلغ الدفع وطريقة الدفع في الفورم)
            paid_amount = request.POST.get('paid_amount')
            payment_method = request.POST.get('payment_method')  # "كاش" أو "بطاقة"

            if paid_amount:
                paid_amount = float(paid_amount)
                Payment.objects.create(
                    invoice=invoice,
                    amount=paid_amount
                )
                invoice.paid_amount = paid_amount
                invoice.save()

            return render(request, 'booking_success.html', {'invoice': invoice})
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
    # الحصول على جميع الفواتير والدفعات
    invoices = Invoice.objects.all().order_by('-date')
    return render(request, 'services/accounting.html', {'invoices': invoices})


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


# صفحة الإحصائيات (عدد المرضى + الحجوزات التي أُدخلت اليوم)
def stats_view(request):
    today = timezone.localdate()  # تاريخ اليوم حسب المنطقة الزمنية

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
