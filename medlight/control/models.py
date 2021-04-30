from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Patients(models.Model):
    #id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', blank=True, null=True)
    full_name = models.CharField('ФИО', max_length=50, default='')
    date = models.DateField('Дата рождения', auto_now_add=False)
    phone = models.CharField('Номер телефона', max_length=13, default='None')

    def __str__(self):
        return '%s %s %s' %(self.full_name, self.date, self.phone)

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'

class Doctors(models.Model):
    #id = models.AutoField(primary_key=True)
    full_name = models.CharField('ФИО', max_length=50, default='None')
    speciality = models.CharField('Специальность', max_length=50, default='')
    qualification = models.CharField('Квалификация', max_length=50, default='')
    phone = models.CharField('Номер телефона', max_length=13, default='None')

    def __str__(self):
        return '%s %s %s %s ' %(self.full_name, self.speciality, self.qualification, self.phone)

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'

class Records(models.Model):
    #id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, blank=True, null=True, related_name='records_patients')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', blank=True, null=True)
    #full_name = models.CharField('ФИО', max_length=50, default='')
    register_date = models.DateTimeField('Время регистрации', auto_now=True)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    payment_status = models.BooleanField('Оплатил')
    used_services = models.CharField('Использованные услуги', max_length=70, default='')
    total_sum = models.IntegerField('Итоговая сумма')
    discharge = models.TextField('Выписка', default='')

    #def __str__(self):
        #return '%s %s %s %s %d' %(self.patient.full_name, self.register_date, self.doctor.full_name, self.payment_status, self.total_sum)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


class Treaments(models.Model):
    speciality = models.CharField('Специальность', max_length=50, default='')
    disease = models.CharField('Болезнь', max_length=30, default='')
    discharge = models.TextField('Выписка', default='')

    def __str__(self):
        return self.disease#, self.speciality, self.discharge

    class Meta:
        verbose_name = 'Стандартное лечение'
        verbose_name_plural = 'Стандартные лечения'

class Pricelist(models.Model):
    service = models.CharField('Услуга', max_length=20, default='')
    price = models.IntegerField('Цена')

    def __str__(self):
        return self.service

    class Meta:
        verbose_name = 'Прайслист'
        verbose_name_plural = 'Прайслист'

class Users(models.Model):
    role = models.CharField('Роль', max_length=20, default='')
    name = models.CharField('Имя Пользователя', max_length=30, default='')
    login = models.CharField('Логин', max_length=50, default='')
    password = models.CharField('Пароль', max_length=50, default='')
    create = models.BooleanField('Создание', default=False)
    delete = models.BooleanField('Удаление', default=False)
    edit = models.BooleanField('Редактирование', default=False)
    view = models.BooleanField('Просмотр', default=False)

    def __str__(self):
        return self.name#self.role, self.login, self.password, self.create, self.delete, self.edit, self.view

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'



