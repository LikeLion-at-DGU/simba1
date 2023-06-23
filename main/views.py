from django.shortcuts import render, redirect, get_object_or_404
from benefits.models import Benefit
from welfare.models import Welfare
from django.utils import timezone


def intro(request):
    return render(request, 'main/intro.html')

def mainpage(request):
    return render(request, 'main/mainpage.html')


