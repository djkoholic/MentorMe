from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import SignUpForm, QuestionForm
from .models import User
from .nlp import convert_to_df
# Create your views here.

def question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        print(convert_to_df(User.objects.filter(user_type='ME').all()))
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = QuestionForm()
    return render(request, 'prototype/question.html', {'form': form})

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