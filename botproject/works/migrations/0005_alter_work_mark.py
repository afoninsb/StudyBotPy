# Generated by Django 4.1 on 2022-08-10 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0004_alter_work_krout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='mark',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
