from django.shortcuts import render, redirect
from .models import Patients, Records
from django.urls import reverse

from django.views.generic import ListView, DetailView
from .forms import RecordForm

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

def edit_page(request):
    success = False
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            success = True

    template = 'control/edit_page.html'
    context = {
        'list_records': Records.objects.all().order_by('-register_date'),
        'form':RecordForm(),
        'success':success
    }
    return render(request, template, context)

def update_page(request, pk):
    get_record = Records.objects.get(pk=pk)
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=get_record)
        if form.is_valid():
            form.save()
    template = 'control/edit_page.html'

    context = {
        'get_record': get_record,
        'update_status': True,
        'form': RecordForm(instance=get_record),
    }
    return render(request, template, context)


def delete_page(request, pk):
    get_record = Records.objects.get(pk=pk)
    get_record.delete()
    return redirect(reverse('edit_page'))
