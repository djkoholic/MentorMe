from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import SignUpForm
from .models import User
# Create your views here.

def index(request):
    return render(request, "prototype/index.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request, "prototype/login.html", {"message": "Invalid Credentials"}
            )
    return render(request, "prototype/login.html")

def sign_up(request):
    if request.method == "POST":
        fn = request.POST["first_name"]
        ln = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        new_user = User.objects.create_user(fn, ln, email, password)
        new_user.save()
        user = authenticate(request, email=email, password=password)
        login(request, user)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'prototype/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))