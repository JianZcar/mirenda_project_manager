from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Project, CustomUser, Task
from .forms import ProjectForm, CustomUserCreationForm, TaskForm

from django.shortcuts import get_object_or_404


@login_required
def home_view(request):
    form = ProjectForm(request=request)  # pass the request object when creating an instance of the form
    projects = Project.objects.filter(members=request.user)  # fetch only projects where the current user is a member
    return render(request, 'home.html', {'projects': projects, 'form': form})
    # pass the form and the projects to the template


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
        else:
            form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def project_view(request, pk):  # add 'pk' as an argument
    project = get_object_or_404(Project, pk=pk)  # use 'pk' to fetch the project
    tasks = project.task_set.all()  # fetch the tasks related to the project
    members = project.members.all()  # fetch the members of the project
    form = TaskForm(project=project)  # pass the project instance when creating an instance of the form
    return render(request, 'project.html', {'project': project, 'tasks': tasks, 'form': form,
                                            'members': members})


def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request=request)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            users = form.cleaned_data.get('users')
            for user in users:
                project.members.add(user)
            project.members.add(request.user)  # add the current user to the project's members
            return redirect('home')
    else:
        form = ProjectForm(request=request)
    return render(request, '', {'form': form})


def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.instance.project = get_object_or_404(Project, pk=request.POST.get('project'))
            # set the project before saving the form
            form.save()
            return redirect('project_view', pk=form.instance.project.pk)
        else:
            print(form.errors)  # print form errors if the form is not valid
    return redirect('home')


@login_required
def mark_task_as_done(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user in task.assigned_to.all():  # check if the current user is assigned to the task
        task.completed = True
        task.completed_by = request.user
        task.save()
    return redirect('project_view', pk=task.project.pk)


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user in task.assigned_to.all():  # check if the current user is assigned to the task
        task.delete()
    return redirect('project_view', pk=task.project.pk)


@login_required
def remove_member(request, pk):
    member = get_object_or_404(CustomUser, pk=pk)
    project = get_object_or_404(Project, members=member)
    project.members.remove(member)
    return redirect('project_view', pk=project.pk)


@login_required
def add_member(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = get_object_or_404(CustomUser, username=username)
            project.members.add(user)
        except Http404:
            pass
        return redirect('project_view', pk=project.pk)


@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('home')
