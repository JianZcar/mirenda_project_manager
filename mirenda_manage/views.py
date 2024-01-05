from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Project
from .forms import ProjectForm

from django.shortcuts import get_object_or_404


@login_required
def home_view(request):
    form = ProjectForm()  # create an instance of the form
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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def project_view(request, pk):  # add 'pk' as an argument
    project = get_object_or_404(Project, pk=pk)  # use 'pk' to fetch the project
    return render(request, 'project.html', {'project': project})


def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)  # create a project instance but don't save it to the database yet
            project.save()  # save the project to the database
            project.members.add(request.user)  # add the current user to the project's members
            return redirect('home')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})
