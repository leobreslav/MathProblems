from django import forms

from Problems.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['body', 'ans', 'source']
        labels = {
            'body': 'Условие',
            'ans': 'Ответ',
            'source': 'Источник'
        }