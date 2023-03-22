import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Others(forms.Form):
    others_=forms.CharField(max_length=300)
    #email_=forms.CharField(max_length=100)

#class RegisterForm(UserCreationForm):
#    email = forms.EmailField(required=True)
#
#    class Meta:
#        model = User
#        fields = ['username', 'email', 'password1', 'password2']