from django.contrib import admin
from django.core.mail import send_mail
from django.utils.html import format_html
from django.urls import reverse
from .models import Doctor, Appointment, Patient, Notification, AccountingItem, DoctorSchedule, Invoice

# ------------------ Doctor ------------------
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty')

# ------------------ Appointment ------------------
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'doctor', 'date', 'time', 'message', 'service_price')
    fields = ('name', 'phone', 'doctor', 'date', 'time', 'service_price', 'message')
    list_filter = ('doctor', 'date')
    search_fields = ('name', 'phone', 'doctor__name')

# ------------------ Patient ------------------
# إزالة أي تسجيل سابق لموديل Patient
try:
    admin.site.unregister(Patient)
except admin.sites.NotRegistered:
    pass

@admin.action(description="إرسال تنبيه لجميع المرضى")
def send_email_notification(modeladmin, request, queryset):
    for patient in queryset:
        send_mail(
            subject='تنبيه من العيادة',
            message='مرحباً، هذا تنبيه مهم لك!',
            from_email='your_email@gmail.com',  # ضع بريدك هنا
            recipient_list=[patient.email],
            fail_silently=False,
        )
    modeladmin.message_user(request, "تم إرسال الرسائل لجميع المرضى!")

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    actions = [send_email_notification]

# ------------------ Notification ------------------
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'message')

# ------------------ AccountingItem ------------------
# إزالة أي تسجيل سابق لموديل AccountingItem
try:
    admin.site.unregister(AccountingItem)
except admin.sites.NotRegistered:
    pass

admin.site.register(AccountingItem)

# ------------------ DoctorSchedule ------------------
@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'hall')

# ------------------ Invoice ------------------
# إزالة أي تسجيل سابق لموديل Invoice
try:
    admin.site.unregister(Invoice)
except admin.sites.NotRegistered:
    pass

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'total_amount', 'paid_amount', 'remaining_amount', 'print_invoice')
    search_fields = ('number',)
    list_filter = ('date',)

    def print_invoice(self, obj):
        url = reverse('print_invoice', args=[obj.id])
        return format_html('<a class="button" href="{}" target="_blank">طباعة</a>', url)

    print_invoice.short_description = 'طباعة الفاتورة'
