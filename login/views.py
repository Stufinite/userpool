from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm

from .forms import UserCreateForm, UserModifyForm, UserForgotPasswordForm

DOMAIN = 'stufinite.faith'


def index(request):
    return redirect('/accounts/login/')


def login(request):
    """
    View that catch request and send it to default login service
    and implement a next_page handler
    """
    from django.contrib.auth import views as auth_views

    response = auth_views.login(request, template_name='login.html')

    if request.user.is_anonymous:
        # The default response of django.contrib.auth.views.login
        return response
    else:
        # Custom cross-site next_page handler
        if request.GET.get('next-page') != None:
            next_page_element = request.GET.get('next-page', '').split('-')
            if len(next_page_element) < 3:
                next_page = 'http://' + DOMAIN
            elif next_page_element[1] + '.' + next_page_element[2] != DOMAIN:
                next_page = 'http://' + DOMAIN
            elif next_page_element[1] + '.' + next_page_element[2] == DOMAIN:
                next_page = 'http://' + next_page_element[0] + '.' + DOMAIN
            else:
                next_page = 'http://' + DOMAIN
            return HttpResponseRedirect(next_page)
        else:
            return response


def register(request):
    """
    View that respond a custom UserCreationForm
    """
    if request.user.is_anonymous:
        if request.method == 'POST':
            form = UserCreateForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                return render(request, 'success.html', {'title': '註冊成功', 'context': '恭喜你成功註冊小幫手'})
        else:
            form = UserCreateForm()
        return render(request, 'register.html', {'form': form})
    else:
        next_page = 'http://' + DOMAIN
        return HttpResponseRedirect(next_page)


def forgot_password(request):
    """
    View that send a new password to a registered email
    """
    if not request.user.is_anonymous:
        next_page = 'http://' + DOMAIN
        return HttpResponseRedirect(next_page)

    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST.get('email'))
            if user.first_name == request.POST.get('first_name') and user.last_name == request.POST.get('last_name'):
                password = User.objects.make_random_password()
                user.set_password(password)

                from django.core.mail import EmailMessage
                from django.template import Context
                from django.template.loader import get_template

                subject, from_email, to = '密碼變更＠選課小幫手', 'noreply@mail.stufinite.faith', user.email
                html_content = get_template(
                    'email/forgotpassword.html').render(Context({'password': password}))
                msg = EmailMessage(subject, html_content, from_email, [to])
                msg.content_subtype = "html"
                msg.send()

                user.save()

                return render(request, 'success.html', {'title': '密碼已寄送', 'context': '前往信箱取得新的密碼'})
            else:
                raise User.DoesNotExist
        except User.DoesNotExist:
            form = UserForgotPasswordForm()
            return render(request, 'forgot.html', {'form': form, 'type_error': True})
    else:
        form = UserForgotPasswordForm()
        return render(request, 'forgot.html', {'form': form})


@login_required
def profile_info(request):
    """
    View that shows user profile
    """
    return render(request, 'profile/info.html', {'userprofile': request.user.userprofile})


@login_required
def profile_password(request):
    """
    View that allow user to change password
    """
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile/password.html', {'form': form})


@login_required
def profile_edit(request):
    """
    View that allow user to edit profile
    """
    user = request.user

    if request.method == 'POST':
        form = UserModifyForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return render(request, 'profile/success.html')

    form = UserModifyForm(user, initial={
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'grade': user.userprofile.grade,
        'major': user.userprofile.major
    })
    return render(request, 'profile/edit.html', {'form': form})
