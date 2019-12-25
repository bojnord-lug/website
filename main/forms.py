from django import forms
from django.contrib.auth.models import User

class Sign_in(forms.Form):
    name=forms.CharField(max_length=20)
    email=forms.EmailField()
    passwd=forms.CharField()

class Log_in(forms.Form):
    username=forms.CharField(max_length=14)
    passwd=forms.CharField()
