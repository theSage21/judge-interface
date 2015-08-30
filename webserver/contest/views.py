from django.shortcuts import render
from contest.forms import RegistrationForm
from question.models import Profile


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
