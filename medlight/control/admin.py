from django.contrib import admin
from .models import Records, Patients

admin.site.register(Patients)
admin.site.register(Records)
# Register your models here.
