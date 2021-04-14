from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeListView.as_view(), name='control_home'),
    #path('', views.MedlightLoginView.as_view(), name='login_page'),
    path('tmp/<int:pk>', views.HomeDetailView.as_view()),
    path('tmp/<int:pk>/detail/<int:id>', views.RecordsDetailView.as_view(), name='detail_page'),
    path('edit-page', views.RecordCreateView.as_view(), name='edit_page'),
    path('update-page/<int:pk>', views.RecordUpdateView.as_view(), name='update_page'),
    path('delete-page/<int:pk>', views.RecordDeleteView.as_view(), name='delete_page'),
    path('login', views.MedlightLoginView.as_view(), name='login_page'),
    path('logout', views.MedlightLogoutView.as_view(), name='logout_page'),
]