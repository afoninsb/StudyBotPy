# Generated by Django 4.0.5 on 2022-07-13 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_alter_spisok_chat'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='spisok',
            options={'ordering': ['last_name']},
        ),
        migrations.AlterField(
            model_name='group',
            name='pin',
            field=models.IntegerField(blank=True, default='', verbose_name='Пин-код'),
        ),
    ]
