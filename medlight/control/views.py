from django.http import request
from django.conf import settings
from .models import Patients, Records, ServicesList, Treaments
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.shortcuts import resolve_url

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from .forms import RecordForm, AuthUserForm, PatientForm, ServiceForm, TreatmentForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


def home_page(request):
    return render(request, 'control/index.html')




#class HomeDetailView(DetailView):
    #model = Patients
    #template_name = 'control/tmp.html'
    #context_object_name = 'get_patient'

#class RecordsDetailView(DetailView):
    #model = Records
    #template_name = 'control/detail.html'
    #context_object_name = 'get_record'

class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False
    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)
    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)

#class PatientsListView(ListView):
    #login_url = reverse_lazy('login_page')
    #model = Patients
    #template_name = 'control/patients.html'
    #context_object_name = 'patients'

class PatientCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login_page')
    model = Patients
    template_name = 'control/patients.html'
    form_class = PatientForm
    success_url = reverse_lazy('patients_page')
    success_msg = 'Пациент создан'
    def get_context_data(self, **kwargs):
        kwargs['list_patients'] = Patients.objects.all()
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

class PatientUpdateView(LoginRequiredMixin, CustomSuccessMessageMixin, UpdateView):
    model = Patients
    template_name = 'control/patients.html'
    form_class = PatientForm
    success_url = reverse_lazy('patients_page')
    success_msg = 'Запись обновлена'
    def get_context_data(self, **kwargs):
        kwargs['update_status'] = True
        return super().get_context_data(**kwargs)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        #print(kwargs['instance'].author)
        #print(self.request.user)
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs

class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patients
    template_name = 'control/patients.html'
    success_url = reverse_lazy('patients_page')
    success_msg = 'Запись удалена'
    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_msg)
        return super().post(request)
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.author:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class PatientDetailView(FormMixin, CustomSuccessMessageMixin, DetailView):
    model = Patients
    template_name = 'control/patients.html'
    context_object_name = 'get_patient'
    form_class = RecordForm
    success_msg = 'Запись создана'
    success_url = reverse_lazy('patients_page')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.patient = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['create_record'] = True
        kwargs['list_services'] = ServicesList.objects.all()
        kwargs['list_treatments'] = Treaments.objects.all()
        return super().get_context_data(**kwargs)

class RecordsListView(ListView):
    model = Records
    template_name = 'control/records.html'
    context_object_name = 'get_records'

class RecordUpdateView(LoginRequiredMixin, CustomSuccessMessageMixin, UpdateView):
    model = Records
    template_name = 'control/records.html'
    form_class = RecordForm
    success_url = reverse_lazy('records_page')
    success_msg = 'Запись обновлена'
    def get_context_data(self, **kwargs):
        kwargs['update_record_status'] = True
        return super().get_context_data(**kwargs)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        #print(kwargs['instance'].author)
        #print(self.request.user)
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs

class RecordDeleteView(LoginRequiredMixin, DeleteView):
    model = Records
    template_name = 'control/records.html'
    success_url = reverse_lazy('records_page')
    success_msg = 'Запись удалена'
    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_msg)
        return super().post(request)
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.author:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

class RecordDetailView(FormMixin, DetailView):
    model = Records
    template_name = 'control/records.html'
    form_class = RecordForm
    context_object_name = 'get_record'

    def get_context_data(self, **kwargs):
        kwargs['show_record_status'] = True
        return super().get_context_data(**kwargs)

class ServicesCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login_page')
    model = ServicesList
    template_name = 'control/services.html'
    form_class = ServiceForm
    success_url = reverse_lazy('services_page')
    #success_msg = 'Пациент создан'
    def get_context_data(self, **kwargs):
        kwargs['list_services'] = ServicesList.objects.all()
        #kwargs['create_record'] = True
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ServiceUpdateView(LoginRequiredMixin, CustomSuccessMessageMixin, UpdateView):
    model = ServicesList
    template_name = 'control/services.html'
    form_class = ServiceForm
    success_url = reverse_lazy('services_page')
    #success_msg = 'Запись обновлена'
    def get_context_data(self, **kwargs):
        kwargs['update_status'] = True
        return super().get_context_data(**kwargs)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        #print(kwargs['instance'].author)
        #print(self.request.user)
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs

class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = ServicesList
    template_name = 'control/services.html'
    success_url = reverse_lazy('services_page')
    success_msg = 'Услуга удалена'
    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_msg)
        return super().post(request)
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.author:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)



class TreatmentCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login_page')
    model = Treaments
    template_name = 'control/treatments.html'
    form_class = TreatmentForm
    success_url = reverse_lazy('treatments_page')
    #success_msg = 'Пациент создан'
    def get_context_data(self, **kwargs):
        kwargs['list_treatments'] = Treaments.objects.all()
        #kwargs['create_record'] = True
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class TreatmentUpdateView(LoginRequiredMixin, CustomSuccessMessageMixin, UpdateView):
    model = Treaments
    template_name = 'control/treatments.html'
    form_class = TreatmentForm
    success_url = reverse_lazy('treatments_page')
    #success_msg = 'Запись обновлена'
    def get_context_data(self, **kwargs):
        kwargs['update_status'] = True
        return super().get_context_data(**kwargs)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        #print(kwargs['instance'].author)
        #print(self.request.user)
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs

class TreatmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Treaments
    template_name = 'control/treatments.html'
    success_url = reverse_lazy('treatments_page')
    success_msg = 'Лечение удалено'
    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_msg)
        return super().post(request)
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.author:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

class TreatmentDetailView(FormMixin, DetailView):
    model = Treaments
    template_name = 'control/treatments.html'
    form_class = RecordForm
    context_object_name = 'get_treatment'

    def get_context_data(self, **kwargs):
        kwargs['show_treatment_status'] = True
        return super().get_context_data(**kwargs)


class MedlightLogoutView(LogoutView):
    next_page = reverse_lazy('login_page') #указываем страницу куда перейдем после логаута


def logout_then_login(request):
    """
    Log out the user if they are logged in. Then redirect to the login page.
    """
    login_url = resolve_url(settings.LOGIN_URL)
    return LogoutView.as_view(next_page=login_url)(request)

class MedlightLoginView(LoginView):
    template_name = 'control/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('control_home')
    #def get_success_url(self):
        #self.success_url


