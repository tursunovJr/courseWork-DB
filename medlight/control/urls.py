from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeListView.as_view(), name='control_home'),
    path('tmp/<int:pk>', views.HomeDetailView.as_view()),
    path('tmp/<int:pk>/detail/<int:id>', views.RecordsDetailView.as_view(), name='detail_page'),
    path('edit-page', views.edit_page, name='edit_page'),
    path('update-page/<int:pk>', views.update_page, name='update_page'),
    path('delete-page/<int:pk>', views.delete_page, name='delete_page'),
]