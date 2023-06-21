from django.shortcuts import render, redirect
from django.contrib.auth import  login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
# from .utils import check_group
# from core.decerators import group_required

def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user:
                login(request, user)
                return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('login')
