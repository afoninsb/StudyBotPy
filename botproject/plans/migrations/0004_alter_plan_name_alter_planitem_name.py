# Generated by Django 4.0.5 on 2022-08-02 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0003_alter_plan_name_alter_planitem_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='name',
            field=models.CharField(max_length=33, verbose_name='Название плана'),
        ),
        migrations.AlterField(
            model_name='planitem',
            name='name',
            field=models.CharField(max_length=33, verbose_name='Название темы'),
        ),
    ]
