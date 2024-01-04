from django.shortcuts import render

# Create your views here.


def base_view(request):
    return render(request, 'base.html')


def home_view(request):
    return render(request, 'home.html')


def login_view(request):
    return render(request, 'login.html')