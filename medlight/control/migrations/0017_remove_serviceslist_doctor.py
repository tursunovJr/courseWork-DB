# Generated by Django 3.2 on 2021-05-03 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0016_auto_20210502_1736'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceslist',
            name='doctor',
        ),
    ]
