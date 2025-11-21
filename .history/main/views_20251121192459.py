from django.db import models
from django.utils import timezone


# ---------------------- Doctors ----------------------
class Doctor(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم الطبيب")
    specialty = models.CharField(max_length=100, verbose_name="التخصص")

    class Meta:
        verbose_name = "طبيب"
        verbose_name_plural = "الأطباء"

    def __str__(self):
        return f"{self.name} - {self.specialty}"


# ---------------------- Patients ----------------------
class Patient(models.Model):

    GENDER_CHOICES = (
        ("ذكر", "ذكر"),
        ("أنثى", "أنثى"),
    )

    name = models.CharField(max_length=100, verbose_name="اسم المريض")
    age = models.IntegerField(blank=True, null=True, verbose_name="العمر")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="الجنس")
    phone = models.CharField(max_length=15, verbose_name="رقم الهاتف")
    disease = models.CharField(max_length=200, verbose_name="المرض أو الحالة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التسجيل")
    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات")

    class Meta:
        verbose_name = "مريض"
        verbose_name_plural = "المرضى"

    def __str__(self):
        return self.name


# ---------------------- Appointment ----------------------
class Appointment(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم المريض")
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="الطبيب")
    date = models.DateField(verbose_name="تاريخ الموعد")
    time = models.TimeField(verbose_name="الوقت")
    message = models.TextField(blank=True, null=True, verbose_name="ملاحظات")
    service_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="سعر الكشف")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاريخ الإنشاء")

    class Meta:
        verbose_name = "موعد"
        verbose_name_plural = "المواعيد"

    def __str__(self):
        return f"موعد {self.name} مع {self.doctor.name} بتاريخ {self.date}"


# ---------------------- Invoice ----------------------
class Invoice(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, null=True, blank=True, verbose_name="الموعد المرتبط")
    number = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="رقم الفاتورة")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="إجمالي المبلغ")
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="المدفوع")
    date = models.DateField(default=timezone.now, verbose_name="تاريخ الفاتورة")

    class Meta:
        verbose_name = "فاتورة"
        verbose_name_plural = "الفواتير"

    @property
    def remaining_amount(self):
        return self.total_amount - self.paid_amount

    def __str__(self):
        if self.appointment:
            return f"فاتورة {self.number} - {self.appointment.name}"
        return f"فاتورة {self.number} - بدون موعد"


# ---------------------- Payment ----------------------
class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="payments", null=True, blank=True, verbose_name="الفاتورة")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المبلغ المدفوع")
    paid_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الدفع")

    class Meta:
        verbose_name = "دفعة"
        verbose_name_plural = "الدفعات"

    def __str__(self):
        if self.invoice:
            return f"{self.amount} د.ل - فاتورة {self.invoice.number}"
        return f"{self.amount} د.ل"


# ---------------------- Notification ----------------------
class Notification(models.Model):
    title = models.CharField(max_length=200, verbose_name="العنوان")
    message = models.TextField(verbose_name="الرسالة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")
    is_active = models.BooleanField(default=True, verbose_name="نشط؟")

    class Meta:
        verbose_name = "إشعار"
        verbose_name_plural = "الإشعارات"

    def __str__(self):
        return self.title


# ---------------------- Accounting ----------------------
class AccountingItem(models.Model):
    date = models.DateField(verbose_name="التاريخ")
    income = models.FloatField(verbose_name="الإيرادات")
    expense = models.FloatField(verbose_name="المصروفات")

    class Meta:
        verbose_name = "سجل مالي"
        verbose_name_plural = "الحسابات المالية"

    def __str__(self):
        return f"{self.date} - دخل: {self.income} | مصروف: {self.expense}"


# ---------------------- Doctor Schedule ----------------------
class DoctorSchedule(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم الطبيب")
    hall = models.CharField(max_length=50, verbose_name="القاعة")
    start_time = models.TimeField(verbose_name="بداية الدوام")
    end_time = models.TimeField(verbose_name="نهاية الدوام")

    class Meta:
        verbose_name = "جدول طبيب"
        verbose_name_plural = "جداول الأطباء"

    def __str__(self):
        return f"{self.name} ({self.hall})"
