#-*- coding:utf8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from login.models import UserProfile
from login.choices import *


class UserCreateForm(UserCreationForm):
    username = forms.RegexField(label="帳號名稱", max_length=30,
                                regex=r'^[A-Za-z0-9]+$',
                                help_text="必填項目，帳號格式為至少六個字元並少於三十個字元的英數以及 _ 的混合",
                                error_messages={
                                    'invalid': "帳號格式為至少六個字元並少於三十個字元的英數以及 _ 的混合"
                                })

    school_email = forms.EmailField(
        label='學校提供的信箱',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 's123456789@mail.nchu.edu.tw'
        })
    )
    first_name = forms.CharField(label='名字', max_length=20, required=True)
    last_name = forms.CharField(label='姓氏', max_length=20, required=True)

    school = forms.ChoiceField(label='就讀學校',
                               choices=SCHOOL_CHOICES, widget=forms.Select(), required=True)
    career = forms.ChoiceField(label='學制',
                               choices=CAREER_CHOICES, initial='U', widget=forms.Select(), required=True)
    major = forms.ChoiceField(label='就讀科系',
                              choices=MAJOR_CHOICES, initial='資訊科學與工程學系學士班', widget=forms.Select(), required=True)
    second_major = forms.ChoiceField(label='雙主修科系',
                                     choices=SECOND_MAJOR_CHOICES, initial='None', widget=forms.Select(), required=True)
    grade = forms.IntegerField(label='年級', initial=1, min_value=1, max_value=7)

    class Meta:
        model = User
        fields = ('username', 'school_email', 'first_name', 'last_name', 'password1',
                  'password2', 'school', 'career', 'major', 'second_major', 'grade')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not (30 > len(username) > 6):
            raise ValidationError("帳號格式為至少六個字元並少於三十個字元的英數以及 _ 的混合！")
        elif username.isdigit():
            raise ValidationError("帳號格式為至少六個字元並少於三十個字元的英數以及 _ 的混合！")
        return username

    def clean_school_email(self):
        email = self.cleaned_data["school_email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("此信箱地址已經被註冊了喔！")
        elif email.split('@')[1] != 'mail.nchu.edu.tw':
            raise ValidationError("目前只開放使用 mail.nchu.edu.tw 進行註冊喔！")
        elif len(email.split('@')[0]) != 10 or email.split('@')[0][0] not in ['s', 'g', 'd', 'w', 'n']:
            raise ValidationError("信箱格式錯誤！")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        password2 = self.data.get('password2')
        if len(password1) < 8:
            raise ValidationError("密碼格式為至少八個字元！")
        elif password1.isdigit():
            raise ValidationError("請使用英數混合的密碼！")
        elif password1 != password2:
            raise ValidationError("輸入的密碼不一致！")
        return password1

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
    email = forms.EmailField(label='信箱',)
    first_name = forms.CharField(label='名字', max_length=20)
    last_name = forms.CharField(label='姓氏', max_length=20)

    career = forms.ChoiceField(
        label='學制',
        choices=CAREER_CHOICES, widget=forms.Select(), required=True)
    major = forms.ChoiceField(
        label='就讀科系',
        choices=MAJOR_CHOICES, widget=forms.Select(), required=True)
    second_major = forms.ChoiceField(
        label='雙主修科系',
        choices=SECOND_MAJOR_CHOICES, widget=forms.Select(), required=True)
    grade = forms.IntegerField(label='年級', min_value=1, max_value=7)

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
    email = forms.EmailField(label='學校提供的信箱', required=True)
    first_name = forms.CharField(label='註冊使用的名字', max_length=20)
    last_name = forms.CharField(label='註冊使用的姓氏', max_length=20)

    class Meta:
        fields = ('email', 'first_name', 'last_name')
