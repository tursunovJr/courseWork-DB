from django.urls import path
from . import views

urlpatterns = [
    path('', views.control_home, name='control_home')
]