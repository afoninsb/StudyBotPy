# Generated by Django 4.1 on 2022-09-13 18:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bots', '0005_alter_botadmin_pin'),
        ('plans', '0005_alter_plan_name_alter_planitem_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Назовите вопрос (для себя)', max_length=255, verbose_name='Название вопроса')),
                ('type', models.CharField(choices=[('1', 'Один правильный'), ('2', 'Несколько правильных'), ('3', 'Текстовый ответ'), ('4', 'Упорядочить')], help_text='Укажите тип вопроса', max_length=1, verbose_name='Тип вопроса')),
                ('text', models.TextField(help_text='Введите текст вопроса', max_length=2000, verbose_name='Текст вопроса')),
                ('img', models.ImageField(blank=True, help_text='Загрузите изображение (.jpg, .png)', upload_to='temp/', verbose_name='Изображение')),
                ('right', models.CharField(max_length=255, verbose_name='Правильный ответ')),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='bots.bot')),
                ('plan', models.ForeignKey(help_text='Укажите тематический план, к которому относится вопрос', on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='plans.plan')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Введите текст ответа', max_length=2000, verbose_name='Текст ответа')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='quizzes.quiz')),
            ],
        ),
    ]
