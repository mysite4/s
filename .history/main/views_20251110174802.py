from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Appointment, Patient
from .forms import AppointmentForm, PatientForm
from django.utils.timezone import now
from datetime import timedelta

# ===========================
# 🏠 الصفحة الرئيسية
# ===========================
def home(request):
    return render(request, 'home.html')


# ===========================
# 📅 صفحة الحجز
# ===========================
def booking_page(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()

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


# ===========================
# 📋 عرض جميع المواعيد
# ===========================
def appointments(request):
    appointments_list = Appointment.objects.all().order_by('-date', '-time')
    return render(request, 'services/appointments.html', {'appointments': appointments_list})


# ===========================
# 👩‍⚕️ عرض وإضافة المرضى
# ===========================
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


# ===========================
# ⚙️ الصفحات الإدارية الأخرى
# ===========================
def accounting(request):
    return render(request, 'services/accounting.html')

def reception(request):
    return render(request, 'services/reception.html')

def notifications(request):
    return render(request, 'services/notifications.html')

def tasks(request):
    return render(request, 'services/tasks.html')

def emergency(request):
    return render(request, 'services/emergency.html')


# ===========================
# ✏️ تعديل موعد باستخدام AJAX
# ===========================
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


# ===========================
# 📊 صفحة الإحصائيات الإدارية
# ===========================
def stats_view(request):
    """
    صفحة الإحصائيات الإدارية 📈
    - إجمالي عدد المرضى المسجلين
    - عدد الزيارات (المواعيد) الخاصة باليوم الحالي
    """

    today = now().date()  # تاريخ اليوم الحالي

    # 🔹 حساب إجمالي المرضى
    total_patients = Patient.objects.count()

    # 🔹 التحقق من نوع الحقل date في نموذج Appointment
    # لو الحقل DateTimeField → نستخدم __date لتصفية اليوم
    try:
        visits_today = Appointment.objects.filter(date__date=today).count()
    except Exception:
        visits_today = Appointment.objects.filter(date=today).count()

    # تمرير البيانات للقالب
    context = {
        'total_patients': total_patients,
        'visits_today': visits_today,
    }

    print(f"📅 عدد الزيارات اليوم = {visits_today}")
    return render(request, 'services/statistics.html', context)
