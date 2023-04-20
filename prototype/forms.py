from django import forms
from .models import User, Skill, Question
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all())
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "user_type", "skills", 'password1', 'password2')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        if commit:
            user.save()
            self.save_m2m()
        return user
    
class QuestionForm(forms.Form):
    title = forms.CharField()
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all())
    class Meta:
        model = Question
        fields = ['title', 'skills']

    def save(self, commit=True):
        question = super(QuestionForm, self).save(commit=False)
        if commit:
            question.save()
            self.save_m2m()
        return question