from django import forms

from .models import Group


class AddGroup(forms.ModelForm):
    """Добавляем группу."""
    class Meta:
        model = Group
        fields = ('name', )
        labels = {'name': 'Название темы', }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
