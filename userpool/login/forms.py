from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User

from login.models import UserProfile
from login.choices import *


class UserCreateForm(UserCreationForm):
    school_email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 's123456789@mail.nchu.edu.tw'
        })
    )
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)

    school = forms.ChoiceField(
        choices=SCHOOL_CHOICES, widget=forms.Select(), required=True)
    career = forms.ChoiceField(
        choices=CAREER_CHOICES, initial='U', widget=forms.Select(), required=True)
    major = forms.ChoiceField(
        choices=MAJOR_CHOICES, initial='資訊科學與工程學系學士班', widget=forms.Select(), required=True)
    second_major = forms.ChoiceField(
        choices=SECOND_MAJOR_CHOICES, initial='None', widget=forms.Select(), required=True)
    grade = forms.IntegerField(initial=1, min_value=1, max_value=7)

    class Meta:
        model = User
        fields = ('username', 'school_email', 'first_name', 'last_name', 'password1',
                  'password2', 'school', 'career', 'major', 'second_major', 'grade')

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit)
        user.email = self.cleaned_data["school_email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        user.userprofile = UserProfile()
        user.userprofile.school_email = self.cleaned_data["school_email"]

        user.userprofile.school = self.cleaned_data["school"]
        user.userprofile.career = self.cleaned_data["career"]
        user.userprofile.major = self.cleaned_data["major"]
        user.userprofile.second_major = self.cleaned_data["second_major"]
        user.userprofile.grade = self.cleaned_data["grade"]

        if commit:
            user.userprofile.save()
            user.save()
        return user


class UserModifyForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    career = forms.CharField(max_length=100)
    major = forms.CharField(max_length=100)
    second_major = forms.CharField(max_length=100)
    grade = forms.IntegerField(min_value=1, max_value=7)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',
                  'career', 'grade', 'major', 'second_major')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(forms.ModelForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.user.email = self.cleaned_data["email"]
        self.user.first_name = self.cleaned_data["first_name"]
        self.user.last_name = self.cleaned_data["last_name"]

        if (not self.user.userprofile):
            self.user.userprofile = UserProfile()
        self.user.userprofile.career = self.cleaned_data["career"]
        self.user.userprofile.grade = self.cleaned_data["grade"]
        self.user.userprofile.major = self.cleaned_data["major"]
        self.user.userprofile.second_major = self.cleaned_data["second_major"]

        if commit:
            self.user.userprofile.save()
            self.user.save()
        return self.user


class UserForgotPasswordForm(forms.Form):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    class Meta:
        fields = ('email', 'first_name', 'last_name')
