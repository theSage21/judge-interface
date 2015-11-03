from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from contest.forms import RegistrationForm
from question.models import Profile
from contest import models


def home(request):
    data = {}
    template = 'contest/home.html'
    return render(request, template, data)


def register(request):
    context = {}
    template = 'contest/register.html'
    context['form'] = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            uname = form['username'].value()
            pwd = form['password'].value()
            p = Profile()
            p.username = uname
            p.set_password(pwd)
            p.save()
            context['successful_registration'] = uname
        else:
            context['form'] = form
    return render(request, template, context)


@login_required
def manage(request, pk):
    if not request.user.is_superuser:
        redirect('403')
    pk = int(pk)
    contest = get_object_or_404(models.ContestControl, pk=pk)


def unauthorized(request):
    return render(request, 'unauthorized.html')
