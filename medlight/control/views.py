from django.http import request
from pytz import unicode
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from slugify import slugify
from django.http import HttpResponse
from django.db.models import Q
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



def getpdf(request):
    record = request.GET.dict()
    patient_name = record["patient_name"]
    patient_birthdate = record["patient_birthdate"]
    patient_phone = record["patient_phone"]
    reg_date = record["reg_date"]
    #print("DATA", reg_date)
    doc_name = record["doc_name"]
    doc_spec = record["doc_spec"]
    disease = record["disease"]
    discharge = record["discharge"]
    total  = ""
    count = 0
    arr = []
    for i in range(len(discharge)):
        if discharge[i] == "'":
            if count == 1:
                arr.append(total)
                count = 0
                total = ""
            count = 1
        elif discharge[i] not in ["'", ",", "[", "]"]:
            total += str(discharge[i])

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=".pdf"'
    p = canvas.Canvas(response)
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    p.setFont('FreeSans', 15)
    #p.setFont("Arial", 20)
    p.drawString(250, 800, "MedLight Clinic")
    p.drawString(10, 760, "ФИО: " + patient_name)
    #p.drawString(10, 740, "Дата Рождения: " + patient_birthdate)
    p.drawString(10, 740, "Номер телефона: " + patient_phone)
    #p.drawString(10, 700, "Дата приёма пациента: " + reg_date)
    p.drawString(10, 700, "ФИО Врача: " + doc_name)
    p.drawString(10, 680, "Специальность Врача: " + doc_spec)
    p.drawString(10, 640, "Диагноз: " + disease)
    p.drawString(250, 600, "Лечение")
    x = 0
    for i in arr:
        if i != " ":
            p.drawString(20, 580 - x, i)
            x += 20
    p.showPage()
    p.save()
    return response



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

class PatientCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView, ListView):
    login_url = reverse_lazy('login_page')
    model = Patients
    template_name = 'control/patients.html'
    form_class = PatientForm
    success_url = reverse_lazy('patients_page')
    success_msg = 'Данные пациента созданы'
    #def get_context_data(self, **kwargs):
        #kwargs['list_patients'] = Patients.objects.all()
        #return super().get_context_data(**kwargs)
    def get_queryset(self):  # новый
        query = self.request.GET.get('q')
        if query is None:
            object_list = Patients.objects.all()
        else:
            object_list = Patients.objects.filter(
                Q(full_name__icontains=query) | Q(date__icontains=query) | Q(phone__icontains=query)
            )
        return object_list
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        slug1 = slugify(form.cleaned_data['full_name'])
        slug2 = slugify(form.cleaned_data['date'].strftime('%Y-%m-%d'))
        slug3 = slugify(form.cleaned_data['phone'])
        if not Patients.objects.filter(full_name=slug1, date=slug2, phone=slug3).exists():
            self.object.save()
            return super().form_valid(form)
        else:
            return self.handle_no_permission()

class PatientUpdateView(LoginRequiredMixin, CustomSuccessMessageMixin, UpdateView):
    model = Patients
    template_name = 'control/patients.html'
    form_class = PatientForm
    success_url = reverse_lazy('patients_page')
    success_msg = 'Данные пациента обновлены'
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
    success_msg = 'Данные пациента удалены'
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
    #success_msg = 'Запись создана'
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
    #context_object_name = 'get_records'
    def get_queryset(self):  # новый
        query = self.request.GET.get('q')
        if query is None:
            object_list = Records.objects.all()
        else:
            object_list = Records.objects.filter(
                Q(patient__full_name__icontains=query) | Q(patient__date__icontains=query) | Q(patient__phone__icontains=query)
                    | Q(register_date__icontains=query) | Q(doctor__full_name__icontains=query) | Q(doctor__speciality__icontains=query)
                    | Q(payment_status__icontains=query) | Q(used_services__icontains=query) | Q(total_sum__icontains=query)
                    | Q(discharge__icontains=query)
            )
        return object_list

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
        if self.request.user != kwargs['instance'].author and (self.request.user.username != 'admin' and self.request.user.password != 'pbkdf2_sha256$260000$2TYARnlkN2c2iEz7KXnlZD$4OpejOwM0qcDD2odV2+trkiPRSV31156RVQEU78WdfU='):
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
        if self.request.user != self.object.author and (self.request.user.username != 'admin' and self.request.user.password != 'pbkdf2_sha256$260000$2TYARnlkN2c2iEz7KXnlZD$4OpejOwM0qcDD2odV2+trkiPRSV31156RVQEU78WdfU='):
            return self.handle_no_permission()
        #if self.request.user != self.object.author:
            #return self.handle_no_permission()
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

class ServicesCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView, ListView):
    login_url = reverse_lazy('login_page')
    model = ServicesList
    template_name = 'control/services.html'
    form_class = ServiceForm
    success_url = reverse_lazy('services_page')
    success_msg = 'Услуга создана'
    #def get_context_data(self, **kwargs):
        #kwargs['list_services'] = ServicesList.objects.all()
        #kwargs['create_status'] = True
        #return super().get_context_data(**kwargs)
    def get_queryset(self):  # новый
        query = self.request.GET.get('q')
        if query is None:
            object_list = ServicesList.objects.all()
        else:
            object_list = ServicesList.objects.filter(
                Q(name__icontains=query) | Q(price__icontains=query)
            )
        return object_list
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        slug1 = slugify(form.cleaned_data['name'])
        #slug2 = slugify(form.cleaned_data['price'])
        if not ServicesList.objects.filter(name=slug1).exists():
            self.object.save()
            return super().form_valid(form)
        else:
            return self.handle_no_permission()

#class ServicesListView(ListView):
    #model = ServicesList
    #template_name = 'control/services.html'
    #queryset = ServicesList.objects.filter(price__icontains='150000')
    #def get_queryset(self):  # новый
        #query = self.request.GET.get('q')
        #if query is None:
            #object_list = ServicesList.objects.all()
        #else:
            #object_list = ServicesList.objects.filter(
                #Q(name__icontains=query) | Q(price__icontains=query)
            #)
        #return object_list


class ServiceUpdateView(LoginRequiredMixin, CustomSuccessMessageMixin, UpdateView):
    model = ServicesList
    template_name = 'control/services.html'
    form_class = ServiceForm
    success_url = reverse_lazy('services_page')
    success_msg = 'Услуга обновлена'
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



class TreatmentCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView, ListView):
    login_url = reverse_lazy('login_page')
    model = Treaments
    template_name = 'control/treatments.html'
    form_class = TreatmentForm
    success_url = reverse_lazy('treatments_page')
    success_msg = 'Стандарное лечение создано'
    #def get_context_data(self, **kwargs):
        #kwargs['list_treatments'] = Treaments.objects.all()
        #kwargs['create_record'] = True
        #return super().get_context_data(**kwargs)
    def get_queryset(self):  # новый
        query = self.request.GET.get('q')
        if query is None:
            object_list = Treaments.objects.all()
        else:
            object_list = Treaments.objects.filter(
                Q(doctor__speciality__icontains=query) | Q(disease__icontains=query) | Q(discharge__icontains=query)
                    | Q(doctor__full_name__icontains=query)
            )
        return object_list
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
    success_msg = 'Стандарное лечение обновлено'
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
    success_msg = 'Стандарное лечение удалено'
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


