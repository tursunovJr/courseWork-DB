from django.db import models
from django.utils import timezone
class Patients(models.Model):
    full_name = models.CharField('ФИО', max_length=50, default='None')
    date = models.DateField('Дата рождения', auto_now_add=False)
    phone = models.CharField('Номер телефона', max_length=13, default='None')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'

class Records(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    full_name = models.CharField('ФИО', max_length=50, default='')
    register_date = models.DateTimeField('Время регистрации', default=timezone.now)
    doctor_type = models.CharField('Тип Врача', max_length=30, default='')
    payment_status = models.BooleanField('Оплатил или нет?')
    used_services = models.CharField('Использованные услуги', max_length=50, default='')
    total_sum = models.CharField('Итого',max_length=50,default='')
    #files = models.FilePathField(path="/home/documents")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

