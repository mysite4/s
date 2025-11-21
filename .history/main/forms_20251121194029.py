from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    # حقول إضافية غير موجودة في الموديل مباشرة
    PAYMENT_CHOICES = (
        ("cash", "كاش"),
        ("card", "بطاقة"),
        ("not_paid", "غير مدفوع"),
    )
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, label="طريقة الدفع")
    paid_amount = forms.DecimalField(label="المبلغ المدفوع الآن", max_digits=10, decimal_places=2, initial=0)

    class Meta:
        model = Appointment
        fields = ['name', 'phone', 'doctor', 'date', 'time', 'message']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # جعل سعر الكشف ثابت عند 500 د.ل
        self.fields['service_price'] = forms.DecimalField(
            label="سعر الكشف (د.ل)",
            max_digits=10,
            decimal_places=2,
            initial=500,
            disabled=True
        )
