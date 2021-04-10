from django.http import request
from .models import Patients, Records
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import RecordForm, AuthUserForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User

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

class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False
    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)
    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)

class RecordCreateView(CustomSuccessMessageMixin, CreateView):
    model = Records
    template_name = 'control/edit_page.html'
    form_class = RecordForm
    success_url = reverse_lazy('edit_page')
    success_msg = 'Запись создана'
    def get_context_data(self, **kwargs):
        kwargs['list_records'] =  Records.objects.all().order_by('-register_date')
        return super().get_context_data(**kwargs)

class RecordUpdateView(CustomSuccessMessageMixin, UpdateView):
    model = Records
    template_name = 'control/edit_page.html'
    form_class = RecordForm
    success_url = reverse_lazy('edit_page')
    success_msg = 'Запись обновлена'
    def get_context_data(self, **kwargs):
        kwargs['update_status'] = True
        return super().get_context_data(**kwargs)

class RecordDeleteView(DeleteView):
    model = Records
    template_name = 'control/edit_page.html'
    success_url = reverse_lazy('edit_page')
    success_msg = 'Запись удалена'
    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_msg)
        return super().post(request)

class MedlightLoginView(LoginView):
    template_name = 'control/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('edit_page')
    #def get_success_url(self):
     #   self.success_url

class MedlightLogoutView(LogoutView):
    next_page = reverse_lazy('edit_page') #указываем страницу куда перейдем после логаута
