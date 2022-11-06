from django import forms
from django.core.exceptions import ValidationError

from .models import Bot, BotAdmin


class AddAdmin(forms.Form):
    tgid = forms.IntegerField(
        label='TelegramID нового админа',
        widget=forms.NumberInput(
                attrs={'class': 'form-control'})
    )
    cur_bot = forms.CharField(widget=forms.HiddenInput())

    def clean(self):
        data = self.cleaned_data['tgid']
        cur_bot = self.cleaned_data['cur_bot']
        err_txt = ''
        if Bot.objects.filter(admins__chat=data).filter(id=cur_bot):
            err_txt = 'Этот TelegramID уже администрирует данного бота'
        elif not BotAdmin.objects.filter(chat=data).count():
            err_txt = 'Такого администратора нет'
        if err_txt:
            self.add_error('tgid', err_txt)
            raise ValidationError('')
        return self.cleaned_data


class BotPass(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ('password', )
        labels = {'password': 'Пароль', }
        widgets = {
            'password': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BotForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ('tg', 'login', 'name')
        labels = {
            'tg': 'Бот-токен',
            'login': 'Имя пользователя бота в Telegram',
            'name': 'Название (для себя)',
        }
        help_texts = {
            'login': ('то, что начинается со знака @.'
                      'Обязательно заканчивается словом bot'),
        }
        widgets = {
            'tg': forms.TextInput(attrs={'class': 'form-control'}),
            'login': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_login(self):
        data = self.cleaned_data['login']
        if data[0] != '@' or data[-3:].lower() != 'bot':
            err_txt = ('Логин бота должен начинаться со знака @ '
                       'и заканчиваться словом bot')
            raise ValidationError(err_txt)
        return data

    def clean_tg(self):
        data = self.cleaned_data['tg']
        if (':' not in data or len(data) < 45
           or not data.split(':')[0].isnumeric()):
            raise ValidationError('Не верный формат токена')
        return data


class BotEditForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ('name', )
        labels = {
            'name': 'Название (для себя)',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
