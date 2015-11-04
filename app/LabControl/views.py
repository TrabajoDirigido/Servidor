from django.shortcuts import render_to_response
from .forms import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json

def index(request):
    form = LoginForm()
    return render_to_response('LabControl/index.html', locals())


def home(request):
    return render_to_response('LabControl/home.html')


def query(request):
    return render_to_response('LabControl/query.html')


def add_lab(request):
    return render_to_response('LabControl/add_lab.html')


def results(request):
    return render_to_response('LabControl/results.html')


def registry(request):
    return JsonResponse({'OK': True})

