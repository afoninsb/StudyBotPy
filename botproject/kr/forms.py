from django import forms
from django.core.exceptions import ValidationError

from kr.models import KR, Task, KROut


class KRAdd(forms.ModelForm):
    """Добавляем и редактируем контрольную работу."""
    class Meta:
        model = KR
        fields = ('name', 'kolzad', 'item')
        help_texts = {
            'name': ('Напишите говорящее значение контрольной работы '
                     '(с номером, с темой)'),
            'kolzad': ('Укажите количество заданий, которое предстоит '
                       'выполнить учащимся'),
            'item': ('Выберите одну тему'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'kolzad': forms.NumberInput(attrs={'class': 'form-control'}),
            'item': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_kolzad(self):
        data = self.cleaned_data['kolzad']
        if data == 0:
            err_txt = ('Укажите число, большее 0')
            raise ValidationError(err_txt)
        return data


class TaskAdd(forms.ModelForm):
    """Добавляем и редактируем задание в контрольную работу."""
    def __init__(self, *args, **kwargs):
        kolzad = kwargs.pop('kolzad')
        super(TaskAdd, self).__init__(*args, **kwargs)
        number = ((i + 1, i + 1) for i in range(kolzad))
        self.fields['number'] = forms.ChoiceField(
            label='Номер задания',
            choices=number,
            widget=forms.Select(attrs={'class': 'form-control'}),
            help_text='Выберите номер задания, к которому принадлежит задача')

    class Meta:
        model = Task
        fields = ('number', 'text', 'img')
        help_texts = {
            'text': ('Введите текст задачи'),
            'img': ('Загрузите изображение .jpg, .png'),
        }
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'img': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
