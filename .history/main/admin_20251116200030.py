from django.contrib import admin
from .models import Doctor, Appointment

# حذف السطر المكرر، واستخدم التسجيل مرة وحدة
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty')  # عرض الاسم والتخصص في لوحة الإدارة

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'doctor', 'date', 'time', 'message')
    list_filter = ('doctor', 'date')
    search_fields = ('name', 'phone', 'doctor__name')

from django.contrib import admin
from .models import Patient

admin.site.register(Patient)

from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'message')
