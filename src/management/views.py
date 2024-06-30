# management/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User  # Import User model
from .models import Project, Task
from .forms import ProjectForm, TaskForm, TaskStatusForm
from django.db.models import Q

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('project_list')
    else:
        return redirect('login')
    
@login_required
def project_list(request):
    projects = Project.objects.filter(Q(owner=request.user) | Q(members=request.user) | Q(tasks__assigned_to=request.user)).distinct()
    return render(request, 'management/project_list.html', {'projects': projects})

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.members.add(request.user)  # Add owner to members
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'management/create_project.html', {'form': form})

@login_required
def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user != project.owner:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'management/update_project.html', {'form': form})

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user != project.owner:
        return HttpResponseForbidden()
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'management/delete_project.html', {'project': project})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user != project.owner and request.user not in project.members.all() and not project.tasks.filter(assigned_to=request.user).exists():
        return HttpResponseForbidden()
    
    tasks = project.tasks.all()
    members = list(project.members.all())
    task_assignees = User.objects.filter(task__project=project).distinct()
    
    for assignee in task_assignees:
        if assignee not in members:
            members.append(assignee)
    
    return render(request, 'management/project_detail.html', {'project': project, 'tasks': tasks, 'members': members})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user != task.assigned_to and request.user != task.project.owner:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = TaskStatusForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskStatusForm(instance=task)
    return render(request, 'management/task_detail.html', {'task': task, 'form': form})

@login_required
def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    users = User.objects.all()
    if request.user != project.owner:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm()
    return render(request, 'management/create_task.html', {'form': form, 'project': project, 'users': users})

@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    project = task.project
    if request.user != project.owner:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'management/update_task.html', {'form': form, 'project': project, 'task': task})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    project = task.project
    if request.user != project.owner:
        return HttpResponseForbidden()
    if request.method == 'POST':
        task.delete()
        return redirect('project_detail', project_id=project.id)
    return render(request, 'management/delete_task.html', {'task': task})

@login_required
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user != task.assigned_to:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = TaskStatusForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskStatusForm(instance=task)
    return render(request, 'management/update_task_status.html', {'form': form, 'task': task})
