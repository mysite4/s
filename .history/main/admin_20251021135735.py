from django.contrib import admin
from .models import Doctor, Appointment

admin.site.register(Doctor)
admin.site.register(Appointment)
from django.contrib import admin
from .models import Doctor, Appointment

admin.site.register(Doctor)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'doctor', 'date', 'time', 'message')
    list_filter = ('doctor', 'date')
    search_fields = ('name', 'phone', 'doctor__name')
