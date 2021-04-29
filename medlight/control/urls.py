from django.urls import path
from . import views

urlpatterns = [
    path('', views.logout_then_login),
    path('home', views.home_page, name= 'home_page'),
    path('home/patients', views.PatientCreateView.as_view(), name='patients_page'),
    path('update-patient/<int:pk>', views.PatientUpdateView.as_view(), name='patients_update_page'),
    path('delete-page/<int:pk>', views.PatientDeleteView.as_view(), name='patients_delete_page'),
    path('create-record/<int:pk>', views.RecordCreateView.as_view(), name='record_create_page'),
    #path('tmp/<int:pk>', views.HomeDetailView.as_view()),
    #path('tmp/<int:pk>/detail/<int:id>', views.RecordsDetailView.as_view(), name='detail_page'),
    #path('create-record', views.RecordCreateView.as_view(), name='record_create_page'),
    #path('update-page/<int:pk>', views.RecordUpdateView.as_view(), name='update_page'),
    #path('delete-page/<int:pk>', views.RecordDeleteView.as_view(), name='delete_page'),
    path('login', views.MedlightLoginView.as_view(), name='login_page'),
    path('logout', views.MedlightLogoutView.as_view(), name='logout_page'),
]