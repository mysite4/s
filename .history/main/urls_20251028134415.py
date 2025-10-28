from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('booking/', views.booking_page, name='booking_page'),
    path('services/appointments/', views.appointments, name='appointments'),
    path('services/patients/', views.patients, name='patients'),
    path('services/accounting/', views.accounting, name='accounting'),
    path('services/reception/', views.reception, name='reception'),
    path('services/notifications/', views.notifications, name='notifications'),
    path('services/statistics/', views.statistics, name='statistics'),
    path('services/tasks/', views.tasks, name='tasks'),
    path('services/emergency/', views.emergency, name='emergency'),
]

