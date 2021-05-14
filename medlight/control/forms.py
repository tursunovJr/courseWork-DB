from django import forms
from .models import Records, Patients, ServicesList, Treaments
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patients
        fields = ('full_name', 'date', 'phone')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class RecordForm(forms.ModelForm):
    class Meta:
        model = Records
        #fields = ('patient', 'doctor', 'payment_status', 'used_services', 'total_sum', 'discharge')
        fields = ('doctor', 'payment_status', 'used_services', 'total_sum', 'discharge', 'disease')
        #labels = {'doctor': 'name', }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class ServiceForm(forms.ModelForm):
    class Meta:
        model = ServicesList
        fields = ('name', 'price')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treaments
        fields = ('doctor', 'disease', 'discharge')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
