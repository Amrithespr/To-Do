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


# Create your views here.



# Function based view


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




def delete(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        project_id = task.project_id
        task.delete()
        return redirect('todoapp:add', id=project_id)
    return render(request, "delete.html" )




def update(request, id):
    task = Task.objects.get(id=id)
    project_id = task.project_id
    form = TodoForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('todoapp:add', id=project_id)
    return render(request, 'edit.html', {'form': form, 'task': task})




def addproject(request,user_id):
    projects = Project.objects.filter(created_by=user_id).annotate(
        total_tasks_count=Count('todos'),
        completed_tasks_count=Count(Case(When(todos__status=True, then=1), output_field=IntegerField()))
    )
    
    if request.method == "POST":
        name2 = request.POST.get('name', '')
        project = Project(title=name2, created_by=request.user)
        project.save()
        return redirect('/addproject/'+ str(request.user.id))
    return render(request, "home2.html", {'projects': projects})

def deleteproject(request, id):
    if request.method == 'POST':
        project = Project.objects.get(id=id)
        project.delete()
        return redirect('/addproject/'+ str(request.user.id))
    return render(request, "deletetwo.html")




def updateproject(request, id):
    project = Project.objects.get(id=id)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('/addproject/'+ str(request.user.id))
    return render(request, 'updateproject.html', {'form': form, 'project': project,})




def updateprojectheading(request, id):
    project = Project.objects.get(id=id)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('todoapp:add', id=id)
    return render(request, 'updateprojectheading.html', {'form': form,'project': project})




      # credentiails

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request, 'Logged in successfully.')
            return redirect('/addproject/'+ str(user.id))
        else:
            messages.error(request,'Invalid username/password')
            return redirect('/login')
    return render(request,'login.html')




def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('/')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken.')
            return redirect('/')
        else:
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
            print('User created')
            messages.success(request, 'Registered successfully.')
            return redirect('/login')
    return render(request,'register.html')




def logout(request):
    auth.logout(request)
    messages.error(request,"logged out successfully")
    return redirect('/login')





@login_required
def export_summary(request, project_id):
    # Get the project and its todos
    project = Project.objects.get(pk=project_id)
    todos = project.todos.all()

    # Count completed and total todos
    completed_count = todos.filter(status=True).count()
    total_count = todos.count()

    # Generate markdown content
    markdown_content = f"# {project.title}\n\n"
    markdown_content += f"**Summary:** {completed_count} / {total_count} todos completed.\n\n"
    markdown_content += "## Pending Tasks\n"
    for todo in todos.filter(status=False):
        markdown_content += f"- [ ] {todo.description}\n"
    markdown_content += "\n## Completed Tasks\n"
    for todo in todos.filter(status=True):
        markdown_content += f"- [x] {todo.description}\n"

    # Save the markdown content locally
    file_name = f"{project.title}.md"
    file_path = os.path.join("ENTER PATH OF FOLDER", file_name)  # Specify the directory where you want to save the markdown file
    with open(file_path, 'w') as file:
        file.write(markdown_content)

    # Create a secret gist using GitHub API
    github_token = "YOUR GITHUB PERSONAL ACCESS TOKEN"  #  Replace with your github personal access token
    headers = {"Authorization": f"token {github_token}"}
    data = {
        "description": f"{project.title} Summary",
        "public": False,
        "files": {
            file_name: {
                "content": markdown_content
            }
        }
    }
    response = requests.post("https://api.github.com/gists", headers=headers, json=data)

    # Check if gist creation was successful
    if response.status_code == 201:
        gist_url = response.json()["html_url"]
        return redirect(gist_url)
    else:
        # Handle error
        return HttpResponse("Failed to export summary as gist.", status=response.status_code)




        # <script src="https://gist.github.com/Amrithespr/25225da0d59102bad55629952ad0e7ee.js"></script>
        # https://gist.github.com/Amrithespr/25225da0d59102bad55629952ad0e7ee

       
        # https://gist.github.com/Amrithespr/6a7df2b733b81827fa39252a610d2310


        # To share (original)
        # https://gist.github.com/Amrithespr/a78966de5a7dbd7bd12a0af87d619197