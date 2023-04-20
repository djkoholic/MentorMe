from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import SignUpForm, QuestionForm
from .models import User
from .nlp import get_recommendation
from django.forms.models import model_to_dict
from django.db.models import Prefetch
# Create your views here.

def question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        users = User.objects.prefetch_related(Prefetch('skills'))
        mentors = users.filter(user_type='ME')
        data = []
        for mentor in mentors:
            mentor_dict = model_to_dict(mentor)
            del mentor_dict['id'], mentor_dict['last_login'], mentor_dict['password'], mentor_dict['user_type'], mentor_dict['is_admin'], mentor_dict['is_staff'], mentor_dict['is_superuser'], mentor_dict['is_active'], mentor_dict['skills']
            skills_values = [skill.name for skill in mentor.skills.all()]
            skills_values_str = ','.join(skills_values)
            mentor_dict['skills'] = skills_values_str
            data.append(mentor_dict)
        
        if form.is_valid():
            skills = form.cleaned_data.get('skills')
            skill_list = [skill.name for skill in skills]
            skill_str = ','.join(skill_list)
            print(get_recommendation(skill_str, data))
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