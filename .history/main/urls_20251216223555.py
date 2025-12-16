from django.urls import path
from . import views
from .views import accounting_dashboard
from .views import print_invoice_view
urlpatterns = [
    path('', views.home, name='home'),
    path('booking/', views.booking_page, name='booking_page'),
    path('services/appointments/', views.appointments, name='appointments'),
    path('services/patients/', views.patients_view, name='patients'),
     path("accounting-dashboard/", accounting_dashboard, name="accounting_dashboard"),
    path('services/reception/', views.reception, name='reception'),
    path('services/notifications/', views.notifications_page, name='notifications'),
    path('services/statistics/', views.stats_view, name='statistics'),  # ✅ تم التعديل هنا
    path('services/tasks/', views.tasks, name='tasks'),
    path('services/emergency/', views.emergency, name='emergency'),
    path('edit_appointment/', views.edit_appointment, name='edit_appointment'),
    path('appointments/add/', views.add_appointment, name='add_appointment'),
    path('invoice/print/<int:invoice_id>/', print_invoice_view, name='print_invoice'),
]
