from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User

from .models import UserProfile


class UserCreateForm(UserCreationForm):
    school_email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 's123456789@mail.nchu.edu.tw'
        })
    )
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ('username', 'school_email', 'first_name', 'last_name', 'password1',
                  'password2')

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit)
        user.email = self.cleaned_data["school_email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        user.userprofile = UserProfile()
        user.userprofile.school_email = self.cleaned_data["school_email"]

        if commit:
            user.userprofile.save()
            user.save()
        return user


class UserModifyForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    grade = forms.IntegerField(min_value=1, max_value=7)
    major = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'grade', 'major')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(forms.ModelForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.user.email = self.cleaned_data["email"]
        self.user.first_name = self.cleaned_data["first_name"]
        self.user.last_name = self.cleaned_data["last_name"]

        if (not self.user.userprofile):
            self.user.userprofile = UserProfile()
        self.user.userprofile.grade = self.cleaned_data["grade"]
        self.user.userprofile.major = self.cleaned_data["major"]

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
