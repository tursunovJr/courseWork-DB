from django.urls import path
from . import views

urlpatterns = [
    path('login', views.MedlightLoginView.as_view(), name='login_page'),
    path('logout', views.MedlightLogoutView.as_view(), name='logout_page'),
    path('', views.logout_then_login),
    path('home', views.home_page, name= 'home_page'),
    path('home/patients', views.PatientCreateView.as_view(), name='patients_page'),
    path('update-patient/<int:pk>', views.PatientUpdateView.as_view(), name='patients_update_page'),
    path('delete-page/<int:pk>', views.PatientDeleteView.as_view(), name='patients_delete_page'),
    path('create-record/<int:pk>', views.PatientDetailView.as_view(), name='record_create_page'),
    path('home/records', views.RecordsListView.as_view(), name='records_page'),
    path('update-record/<int:pk>', views.RecordUpdateView.as_view(), name='record_update_page'),
    path('delete-record/<int:pk>', views.RecordDeleteView.as_view(), name='record_delete_page'),
    path('record/<int:pk>', views.RecordDetailView.as_view(), name='record_detail_page'),
    path('home/services', views.ServicesCreateView.as_view(), name='services_page'),
    #path('home/service/create-service', views.ServicesCreateView.as_view(), name='service_create_page'),
    path('update-service/<int:pk>', views.ServiceUpdateView.as_view(), name='service_update_page'),
    path('delete-service/<int:pk>', views.ServiceDeleteView.as_view(), name='service_delete_page'),
    path('home/treatments', views.TreatmentCreateView.as_view(), name='treatments_page'),
    path('update-treatment/<int:pk>', views.TreatmentUpdateView.as_view(), name='treatments_update_page'),
    path('delete-treatment/<int:pk>', views.TreatmentDeleteView.as_view(), name='treatments_delete_page'),
    path('treatment/<int:pk>', views.TreatmentDetailView.as_view(), name='treatment_detail_page'),
    path('pdf', views.getpdf, name='generate_pdf'),
    #path('create-record/<int:pk>', views.RecordCreateView.as_view(), name='record_create_page'),

    #path('tmp/<int:pk>', views.HomeDetailView.as_view()),
    #path('tmp/<int:pk>/detail/<int:id>', views.RecordsDetailView.as_view(), name='detail_page'),
    #path('create-record', views.RecordCreateView.as_view(), name='record_create_page'),
    #path('update-page/<int:pk>', views.RecordUpdateView.as_view(), name='update_page'),
    #path('delete-page/<int:pk>', views.RecordDeleteView.as_view(), name='delete_page'),

]