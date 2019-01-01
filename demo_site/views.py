import bfa
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.shortcuts import render, redirect


def home(request):
    return render(request, 'demo_site/home.html')


def sign_up(request):
    errors = []

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            fp = bfa.fingerprint.get(request)
            # Activation part
            User.objects.create(username=username, password=fp)
            user = User.objects.get(username=username)
            login(request, user)
            return redirect('home')
        except IntegrityError:
            errors.append('Username already taken')
        except ConnectionError:
            errors.append("Can't download or execute JS")
        except ValueError:
            errors.append("Fingerprint bad value")

    return render(request, 'demo_site/signup.html',
                  {'fp_field': bfa.fingerprint.field,
                   'errors': errors})


def log_in(request):
    errors = []

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            fp = bfa.fingerprint.get(request)
            user = User.objects.get(username=username, password=fp)
            login(request, user)
            return redirect('home')
        except User.DoesNotExist:
            errors.append('Wrong username or fingerprint')
        except ConnectionError:
            errors.append("Can't download or execute JS")
        except ValueError:
            errors.append("Fingerprint bad value")

    return render(request, 'demo_site/login.html',
                  {'fp_field': bfa.fingerprint.field,
                   'errors': errors})


def log_out(request):
    logout(request)
    return redirect('home')
