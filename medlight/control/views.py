from django.shortcuts import render
from .models import Patients, Records

from django.views.generic import ListView, DetailView


class HomeListView(ListView):
    model = Patients
    template_name = 'control/index.html'
    context_object_name = 'patients'

class HomeDetailView(DetailView):
    model = Patients
    template_name = 'control/tmp.html'
    context_object_name = 'get_patient'


class RecordsDetailView(DetailView):
    model = Records
    template_name = 'control/detail.html'
    context_object_name = 'get_record'



