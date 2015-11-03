from django.shortcuts import render
from contest.forms import RegistrationForm
from question.models import Profile
from contest.functions import is_contest_on, contest_phase


def home(request):
    data = {}
    template = 'contest/home.html'
    data['contest_on'] = is_contest_on()
    return render(request, template, data)


def register(request):
    context = {}
    template = 'contest/register.html'
    context['contest_phase'] = contest_phase()
    if contest_phase() != 'after':
        context['form'] = RegistrationForm()
        context['contest_on'] = is_contest_on()
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


def unauthorized(request):
    return render(request, 'unauthorized.html')
