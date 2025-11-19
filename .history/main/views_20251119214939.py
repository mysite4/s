from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Appointment, Patient
from .forms import AppointmentForm, PatientForm
from django.utils import timezone

# الصفحة الرئيسية
def home(request):
    return render(request, 'home.html')


# صفحة الحجز
# صفحة الحجز
def booking_page(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()  # يخزن الموعد

            # الحصول على الملاحظات من الفورم
            patient_name = form.cleaned_data['name']
            patient_phone = form.cleaned_data['phone']
            patient_notes = form.cleaned_data.get('message', '')

            # إنشاء أو تحديث المريض لتخزين الملاحظات
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


# صفحات الخدمات الأخرى (عرض فقط)
def accounting(request):
    return render(request, 'services/accounting.html')

def reception(request):
    return render(request, 'services/reception.html')

def tasks(request):
    return render(request, 'services/tasks.html')

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

    # عدد المرضى الكلي
    total_patients = Patient.objects.count()

    # عدد الحجوزات التي تم إدخالها اليوم
    visits_today = Appointment.objects.filter(created_at__date=today).count()

    context = {
        'total_patients': total_patients,
        'visits_today': visits_today,
    }

    print("📊 الإحصائيات تعمل بنجاح ✅")  # يظهر في التيرمنال لتأكيد التنفيذ
    return render(request, 'services/statistics.html', context)

from django.shortcuts import render
from .models import Notification

def notifications_page(request):
    notifications = Notification.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'services/notifications.html', {'notifications': notifications})
from django.shortcuts import render
from django.db.models import Sum
from .models import Invoice

def accounting_dashboard(request):
    data = Invoice.objects.values('date__month').annotate(total=Sum('amount'))
    
    invoice_labels = [f"Month {item['date__month']}" for item in data]
    income_data = [item['total'] for item in data]

    return render(request, 'services/accounting.html', {
        'invoice_labels': invoice_labels,
        'income_data': income_data,
    })
