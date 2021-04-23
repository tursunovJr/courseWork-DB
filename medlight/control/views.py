from django.http import request
from django.conf import settings
from .models import Patients, Records
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import resolve_url

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import RecordForm, AuthUserForm, PatientForm
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

class RecordsDetailView(DetailView):
    model = Records
    template_name = 'control/detail.html'
    context_object_name = 'get_record'

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


class RecordCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login_page')
    model = Records
    template_name = 'control/edit_page.html'
    form_class = RecordForm
    success_url = reverse_lazy('edit_page')
    success_msg = 'Запись создана'
    def get_context_data(self, **kwargs):
        kwargs['list_records'] = Records.objects.all().order_by('-register_date')
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

class RecordUpdateView(LoginRequiredMixin, CustomSuccessMessageMixin, UpdateView):
    model = Records
    template_name = 'control/edit_page.html'
    form_class = RecordForm
    success_url = reverse_lazy('edit_page')
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

class RecordDeleteView(LoginRequiredMixin, DeleteView):
    model = Records
    template_name = 'control/edit_page.html'
    success_url = reverse_lazy('edit_page')
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


