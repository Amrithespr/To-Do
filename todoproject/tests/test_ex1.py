import pytest


from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

import os
import requests
from django.template import loader

from .models import Task,Project
from .forms import TodoForm, ProjectForm

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.db.models import Count, Case, When, IntegerField

from django.http import HttpResponse




def test_example2():
    assert 1 == 1

def add(request,id):
    task1 = Task.objects.all()
    try:
        project = Project.objects.get(pk=id)
        tasks = Task.objects.filter(project=project)
        
    except Project.DoesNotExist:
        return render(request, "404.html")
    
    form = TodoForm()
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project  # Associate task with the project
            task.save()
            return redirect('todoapp:add', id=id)
    else:
        form = TodoForm()
    return render(request, "home.html", {'task': task1, 'form':form,'tasks': tasks, 'project':project,'project_id':id})

    
