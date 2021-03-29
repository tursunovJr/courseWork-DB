from django.shortcuts import render
from .models import Patients, Records

def control_home(request):
    patients = Patients.objects.order_by('-date')
    return render(request, 'control/index.html', {'patients': patients})