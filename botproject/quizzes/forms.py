from django import forms

from .models import TYPES, Quiz


class AddQuizStep1(forms.Form):
    type = forms.ChoiceField(
        label='Тип вопроса',
        choices=TYPES,
        widget=forms.RadioSelect()
    )
    count = forms.IntegerField(
        label='Количество ответов',
        min_value=1,
    )


class AddQuizStep2(forms.Form):

    def __init__(self, *args, **kwargs):
        count = kwargs.pop('count')
        super(AddQuizStep2, self).__init__(*args, **kwargs)
        for i in range(1, count + 1):
            field = f'answer{i}'
            self.fields[field] = forms.CharField(
                label=f'Ответ {i}',
                widget=forms.TextInput(attrs={'class': 'form-control'}),
            )

    name = forms.CharField(
        label='Название вопроса',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    # count = forms.CharField(
    #     label='Количество ответов',
    #     min_value=1,
    # )
    #     model = Quiz
    #     fields = ('name', 'type', 'plan', 'text', 'img', 'right')
    #     help_texts = {
    #         'name': ('Введите название вопроса (для себя)'),
    #         'plan': ('Укажите тему вопроса'),
    #         'text': ('Введите текст задачи'),
    #         'img': ('Загрузите изображение .jpg, .png'),
    #         'right': ('Укажите правильный'),
    #     }
    #     widgets = {
    #         'text': forms.Textarea(attrs={'class': 'form-control'}),
    #         'img': forms.ClearableFileInput(attrs={'class': 'form-control'}),
    #     }
