from django.shortcuts import render


def home(request):
    return render(request, 'demo_site/home.html')


def signup(request):
    return render(request, 'demo_site/signup.html')


def login(request):
    return render(request, 'demo_site/login.html')
