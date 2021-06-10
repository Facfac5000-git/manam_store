from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm


def login_page(request):
    forms = LoginForm()
    message = ''
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                message = 'Login incorrecto'
    context = {'form': forms, 'message': message}
    return render(request, 'users/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')
