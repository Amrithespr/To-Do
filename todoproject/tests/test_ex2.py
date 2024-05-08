import pytest

from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, related_name='todos', on_delete=models.CASCADE)
    project_id = models.ForeignKey(on_delete=models.deletion.CASCADE, to='todoapp.Project'),

    def __str__(self):
        return self.description