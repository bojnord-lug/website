from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.conf import settings

from .models import Post

import requests


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

class SubmitComment(forms.Form):
    name = forms.CharField(max_length=20)
    text = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    website = forms.CharField(max_length=30, required=False)    
    post = forms.IntegerField()
    captcha = forms.CharField(widget=forms.Textarea)

class UpdateProfileForm(forms.Form):
    first_name = forms.CharField(max_length=15)
    last_name = forms.CharField(max_length=15)
    expertise = forms.CharField(max_length=20)
    photo = forms.ImageField(required=False)
    description = forms.CharField(widget=forms.Textarea)

class CaptchaPasswordResetForm(PasswordResetForm):
    recaptcha = forms.CharField(widget=forms.Textarea)

    def clean_recaptcha(self):
        captcha = self.cleaned_data['recaptcha']
        secret_key = settings.RECAPTCHA_SECRET_KEY

        # captcha verification
        data = {
            'response': captcha,
            'secret': secret_key
        }
        resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result_json = resp.json()
        if not result_json.get('success'):
            raise forms.ValidationError("درخواست تغییر رمز توسط یک ربات ارسال شده است")

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    expertise = forms.CharField(max_length=15)
    email = forms.EmailField()

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']):
            raise forms.ValidationError("حسابی با این ایمیل موجود است")
        return self.cleaned_data['email']
    
class AddPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'category']
