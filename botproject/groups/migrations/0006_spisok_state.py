# Generated by Django 4.1 on 2022-08-08 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0005_alter_group_pin'),
    ]

    operations = [
        migrations.AddField(
            model_name='spisok',
            name='state',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
