from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeListView.as_view(), name='control_home'),
    path('tmp/<int:pk>', views.HomeDetailView.as_view()),
    path('tmp/<int:pk>/detail/<int:id>', views.RecordsDetailView.as_view(), name='detail_page'),

]