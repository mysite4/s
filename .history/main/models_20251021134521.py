from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.specialty}"


class Appointment(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم المريض")
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="الطبيب")
    date = models.DateField(verbose_name="تاريخ الموعد")
    time = models.TimeField(verbose_name="الوقت")
    message = models.TextField(blank=True, null=True, verbose_name="ملاحظات")

    def __str__(self):
        return f"موعد {self.name} مع {self.doctor.name} بتاريخ {self.date}"
