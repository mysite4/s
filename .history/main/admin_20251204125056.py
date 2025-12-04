from django.contrib import admin
from .models import Doctor, Appointment, Patient, Notification, AccountingItem, DoctorSchedule

# Doctor
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty')

# Appointment
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'doctor', 'date', 'time', 'message', 'service_price')
    fields = ('name', 'phone', 'doctor', 'date', 'time', 'service_price', 'message')
    list_filter = ('doctor', 'date')
    search_fields = ('name', 'phone', 'doctor__name')

# Patient
admin.site.register(Patient)

# Notification
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'message')

# AccountingItem
admin.site.register(AccountingItem)

# DoctorSchedule
@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'hall')

from django.contrib import admin
from .models import Invoice  # ← استيراد الموديل

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'total_amount', 'paid_amount', 'remaining_amount')
    search_fields = ('number',)
    list_filter = ('date',)
