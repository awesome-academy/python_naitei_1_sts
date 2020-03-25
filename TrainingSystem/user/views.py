from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import UserRegisterForm, UserUpdateForm
from django.views import View
import json
from django.http import HttpResponse

# Create your views here.
from .models import User
from .token import account_activation_token


def home(request):
    return render(request, 'user/base.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            User = form.save(commit=False)
            User.is_active = False
            User.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('user/acc_active_email.html', {
                'user': User,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(User.pk)),
                'token': account_activation_token.make_token(User),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
            # form.save()
            # messages.success(request, f'Your account has been created! You are now able to log in.')
            # return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {'u_form': u_form}
    return render(request, 'user/profile.html', context)
