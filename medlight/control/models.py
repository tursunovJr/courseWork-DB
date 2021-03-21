from django.db import models

class Patients(models.Model):
    full_name = models.CharField('ФИО', max_length=50, default='None')
    phone = models.CharField('Номер телефона', max_length=13, default='None')
    date = models.DateField

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'

class Records(models.Model):
    patient_id = models.ForeignKey(Patients, on_delete=models.CASCADE)
    full_name = models.CharField('ФИО', max_length=50, default='')
    doctor_type = models.CharField('Тип Врача', max_length=30, default='')
    payed_status = models.BooleanField('Оплатил или нет?')
    total_sum = models.CharField('Итого',max_length=50,default='')
    #files = models.FilePathField(path="/home/documents")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

