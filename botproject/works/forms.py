from django import forms
from django.core.exceptions import ValidationError

from works.models import Work


class ReviewWork(forms.ModelForm):
    """Проверяем работу ученика."""
    class Meta:
        model = Work
        fields = ('status', 'review', 'mark')
        labels = {
            'status': 'Статус работы',
            'review': 'Отзыв на работу',
            'mark': 'Оценка',
        }
        widgets = {
            'status': forms.RadioSelect(),
            'review': forms.Textarea(
                attrs={'class': 'form-control', 'rows': '5'}),
            'mark': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        data_status = self.cleaned_data['status']
        if data_status == 'passed':
            err_txt = ('Выберите один из двух статусов: Работа зачтена '
                       'или Работа отклонена')
            self.add_error('status', err_txt)
            raise ValidationError('')
        return self.cleaned_data
