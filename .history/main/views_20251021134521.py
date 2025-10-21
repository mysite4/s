from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
from django.shortcuts import render

def booking_page(request):
    return render(request, 'booking.html')
from django.shortcuts import render, redirect
from .forms import AppointmentForm

def booking_page(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'booking_success.html')
    else:
        form = AppointmentForm()
    return render(request, 'booking.html', {'form': form})
