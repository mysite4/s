from django.db import models
from django.utils import timezone

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.specialty}"

from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    disease = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True) 
    
    def __str__(self):
        return self.name

class Appointment(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم المريض")
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="الطبيب")
    date = models.DateField(verbose_name="تاريخ الموعد")
    time = models.TimeField(verbose_name="الوقت")
    message = models.TextField(blank=True, null=True, verbose_name="ملاحظات")
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"موعد {self.name} مع {self.doctor.name} بتاريخ {self.date}"

class Payment(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.appointment} - {self.amount} د.ل"

from django.db import models

class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # للتحكم إذا التنبيه يظهر ولا لا

    def __str__(self):
        return self.title

from django.db import models

class AccountingItem(models.Model):
    date = models.DateField()
    income = models.FloatField()
    expense = models.FloatField()

    def __str__(self):
        return f"{self.date} - Income: {self.income} / Expense: {self.expense}"
