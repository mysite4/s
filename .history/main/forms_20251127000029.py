from django import forms
from .models import Appointment, Patient

# ---------------- Appointment Form ----------------
class AppointmentForm(forms.ModelForm):
    PAYMENT_CHOICES = (
        ("cash", "كاش"),
        ("card", "بطاقة"),
        ("not_paid", "غير مدفوع"),
    )
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, label="طريقة الدفع")

    class Meta:
        model = Appointment
        fields = ['name', 'phone', 'doctor', 'date', 'time', 'message']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

# ---------------- Patient Form ----------------
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'phone', 'disease', 'notes']
