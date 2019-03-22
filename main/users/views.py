from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View
from django.contrib import messages
from django.core.exceptions import ValidationError

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html', {"message":None})
    context = {
        "user": request.user
    }
    return render(request,'users/user.html', context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse('index'))
    else:
        messages.warning(request, f'Invalid user')
        return render(request,'users/login.html')

def logout_view(request):
    messages.info(request, f'You, {request.user}, have just logged out!')
    logout(request)
    return render(request, 'users/login.html', {"message": "Logged out."})

class Registration(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'users/registration.html', context={'form': form})

    def post(self, request):
        bound_form = UserCreationForm(request.POST)

        if bound_form.is_valid():
            bound_form.save()
            username = bound_form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}, now log in!')
            return redirect(reverse('index'))
        return render(request, 'users/registration.html', context={'form': bound_form})
