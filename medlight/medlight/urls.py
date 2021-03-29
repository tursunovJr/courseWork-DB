from django.contrib import admin
from django.urls import path, include
#from django.contrib.auth.mixins import LoginRequiredMixin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('control.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

#class MyView(LoginRequiredMixin, View):
    #login_url = '/login/'
    #redirect_field_name = 'redirect_to'
