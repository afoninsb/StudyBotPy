# Generated by Django 4.0.5 on 2022-07-23 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_alter_group_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='pin',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Пин-код'),
        ),
    ]