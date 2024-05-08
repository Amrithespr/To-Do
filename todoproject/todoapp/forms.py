from.models import Task, Project
from django import forms

class TodoForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=['description', 'status']

class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields=['title']
