from django.db import models
from django.utils import timezone

# ---------------------- Doctors ----------------------
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.specialty}"


# ---------------------- Patients ----------------------
class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    disease = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

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
    service_price = models.DecimalField(max_digits=10, decimal_places=2, default=500, verbose_name="سعر الكشف")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"موعد {self.name} مع {self.doctor.name} بتاريخ {self.date}"


# ---------------------- Invoice ----------------------
class Invoice(models.Model):
    appointment = models.OneToOneField(
        Appointment, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    number = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # ← أصبح حقل حقيقي
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateField(default=timezone.now)

    @property
    def remaining_amount(self):
        remaining = self.total_amount - self.paid_amount
        return remaining if remaining > 0 else 0  # يمنع القيم السالبة

    def __str__(self):
        if self.appointment:
            return f"فاتورة {self.number} - {self.appointment.name}"
        return f"فاتورة {self.number} - غير مرتبطة بموعد"


# ---------------------- Payment ----------------------
class Payment(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="payments",
        null=True,
        blank=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.invoice:
            return f"{self.amount} د.ل - {self.invoice.number}"
        return f"{self.amount} د.ل - فاتورة غير محددة"


# ---------------------- Notification ----------------------
class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


# ---------------------- Accounting ----------------------
class AccountingItem(models.Model):
    date = models.DateField()
    income = models.FloatField()
    expense = models.FloatField()

    def __str__(self):
        return f"{self.date} - Income: {self.income} / Expense: {self.expense}"


# ---------------------- Doctor Schedule ----------------------
class DoctorSchedule(models.Model):
    name = models.CharField(max_length=100)
    hall = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.name
