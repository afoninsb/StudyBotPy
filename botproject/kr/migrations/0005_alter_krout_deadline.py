# Generated by Django 4.0.5 on 2022-08-02 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kr', '0004_krout_taskout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='krout',
            name='deadline',
            field=models.DateTimeField(blank=True, default=None, verbose_name='Дедлайн сдачи'),
        ),
    ]
