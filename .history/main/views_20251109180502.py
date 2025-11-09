from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Appointment, Patient
from .forms import AppointmentForm, PatientForm

# الصفحة الرئيسية
def home(request):
    return render(request, 'home.html')

# صفحة الحجز
# صفحة الحجز
def booking_page(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()  # ✅ يخزن الموعد

            # ✅ إنشاء مريض تلقائيًا عند الحجز
            patient_name = appointment.name
            patient_phone = getattr(appointment, 'phone', None)

            # يتحقق إن المريض مش مكرر
            patient, created = Patient.objects.get_or_create(
                name=patient_name,
                defaults={'phone': patient_phone}
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
            form.save()  # ✅ يحفظ المريض في قاعدة البيانات
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

def notifications(request):
    return render(request, 'services/notifications.html')

def statistics(request):
    return render(request, 'services/statistics.html')

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


from django.shortcuts import render
from .models import Patient, Appointment, Payment

def statistics(request):
    # عدد المرضى
    total_patients = Patient.objects.count()

    # الزيارات اليومية (عدد المواعيد اليوم)
    from django.utils import timezone
    today = timezone.now().date()
    daily_visits = Appointment.objects.filter(date=today).count()

    # الحجوزات الجديدة (مثلاً آخر أسبوع)
    from datetime import timedelta
    last_week = today - timedelta(days=7)
    new_appointments = Appointment.objects.filter(date__gte=last_week).count()

    # الإيرادات الشهرية (مثلاً آخر شهر)
    from django.db.models import Sum
    last_month = today - timedelta(days=30)
    monthly_revenue = Payment.objects.filter(date__gte=last_month).aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'total_patients': total_patients,
        'daily_visits': daily_visits,
        'new_appointments': new_appointments,
        'monthly_revenue': monthly_revenue,
    }

    return render(request, 'services/statistics.html', context)
