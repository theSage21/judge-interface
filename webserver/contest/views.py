from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse


def home(request):
    data = {}
    template = 'contest/home.html'
    return render(request, template, data)
