from django import forms
from django.core.exceptions import ValidationError

from .models import Plan, PlanItem


class AddPlan(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ('name', )
        labels = {'name': 'Название темы', }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AddItem(forms.ModelForm):
    class Meta:
        model = PlanItem
        fields = ('name', 'link', 'type')
        labels = {
            'name': 'Название',
            'link': 'Ссылка на материалы',
            'type': 'Тип материала',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        try:
            data_link = self.cleaned_data['link']
        except KeyError:
            raise ValidationError('')
        # data_type = self.cleaned_data['type']
        # if data_type == 'p' and not data_link:
        #     err_txt = 'Для практической работы обязательно указать ссылку!'
        #     self.add_error('link', err_txt)
        #     raise ValidationError('')
        return self.cleaned_data


class EditItem(forms.ModelForm):
    class Meta:
        model = PlanItem
        fields = ('name', 'link')
        labels = {
            'name': 'Название',
            'link': 'Ссылка на материалы',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        try:
            data_link = self.cleaned_data['link']
        except KeyError:
            raise ValidationError('')
        # data_type = self.cleaned_data['type']
        # if data_type == 'p' and not data_link:
        #     err_txt = 'Для практической работы обязательно указать ссылку!'
        #     self.add_error('link', err_txt)
        #     raise ValidationError('')
        return self.cleaned_data
