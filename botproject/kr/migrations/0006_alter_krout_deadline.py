# Generated by Django 4.0.5 on 2022-08-02 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kr', '0005_alter_krout_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='krout',
            name='deadline',
            field=models.DateTimeField(null=True, verbose_name='Дедлайн сдачи'),
        ),
    ]
