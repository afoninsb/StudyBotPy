# Generated by Django 4.1 on 2022-08-11 14:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0007_temp_alter_group_pin'),
        ('works', '0005_alter_work_mark'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='work', to='groups.group'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='work',
            name='status',
            field=models.CharField(choices=[('passed', 'Работа сдана'), ('done', 'Работа зачтена'), ('rejected', 'Работа отклонена')], default='passed', max_length=10),
        ),
    ]
