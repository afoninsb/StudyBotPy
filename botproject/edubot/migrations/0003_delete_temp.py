# Generated by Django 4.1 on 2022-08-19 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edubot', '0002_remove_temp_first_name_remove_temp_last_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Temp',
        ),
    ]