from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import SignUpForm, QuestionForm
from .models import User, Notification, Question
from .nlp import get_recommendation_question, check_similar_questions, get_recommendation_skills
from django.forms.models import model_to_dict
from django.db.models import Prefetch
# Create your views here.
def check(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        questions = Question.objects.all()
        data = []
        for question in questions:
            data.append(model_to_dict(question))
        if form.is_valid():
            question = form.cleaned_data["title"]
            question_ids = check_similar_questions(question, data)
            questions = Question.objects.filter(id__in=question_ids)
            return render(request, 'prototype/question.html', {
                'form': form,
                "flag": True,
                "similar_questions": questions
            })
        

def question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        users = User.objects.prefetch_related(Prefetch('skills'))
        mentors = users.filter(user_type='MO')
        data = []
        for mentor in mentors:
            mentor_dict = model_to_dict(mentor)
            del mentor_dict['id'], mentor_dict['last_login'], mentor_dict['password'], mentor_dict['user_type'], mentor_dict['is_admin'], mentor_dict['is_staff'], mentor_dict['is_superuser'], mentor_dict['is_active'], mentor_dict['skills']
            skills_values = [skill.name for skill in mentor.skills.all()]
            skills_values_str = ','.join(skills_values)
            mentor_dict['skills'] = skills_values_str
            data.append(mentor_dict)
        
        if form.is_valid():
            question = form.save()
            recommendations = get_recommendation_question(question.title, data)
            for email in recommendations:
                user = User.objects.filter(email=email).get()
                notif = Notification(user=user, question=question)
                notif.save()
            return redirect('index')
    else:
        form = QuestionForm()
    return render(request, 'prototype/question.html', {
        'form': form,
        'flag': False
    })

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

def notification(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, "prototype/notification.html", {"notifications": notifications})

def dashboard(request):
    user = User.objects.filter(email=request.user.email).get()
    questions = Question.objects.filter(user=user)
    users = User.objects.prefetch_related(Prefetch('skills'))
    mentors = users.filter(user_type='MO')
    data = []
    for mentor in mentors:
        mentor_dict = model_to_dict(mentor)
        del mentor_dict['id'], mentor_dict['last_login'], mentor_dict['password'], mentor_dict['user_type'], mentor_dict['is_admin'], mentor_dict['is_staff'], mentor_dict['is_superuser'], mentor_dict['is_active'], mentor_dict['skills']
        skills_values = [skill.name for skill in mentor.skills.all()]
        skills_values_str = ','.join(skills_values)
        mentor_dict['skills'] = skills_values_str
        data.append(mentor_dict)
    skill_list = [skill.name for skill in user.skills.all()]
    skills = ','.join(skill_list)
    recommended_mentors = get_recommendation_skills(skills, data)
    return render(request, "prototype/dashboard.html", {
        "questions": questions,
        "mentors": recommended_mentors
    })