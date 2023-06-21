from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    description = forms.CharField()
    class Meta:
        model = Task
        fields = ['description']