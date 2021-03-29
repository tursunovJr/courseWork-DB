from django.contrib import admin
from .models import Records, Patients, Users, Doctors, Pricelist, Treaments

admin.site.register(Patients)
admin.site.register(Records)
admin.site.register(Users)
admin.site.register(Doctors)
admin.site.register(Pricelist)
admin.site.register(Treaments)
# Register your models here.
