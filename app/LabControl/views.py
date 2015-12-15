from django.shortcuts import render_to_response,render
from .forms import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from ServerClient.models import Lab, Result, Query, SubQuery
import re
from django.core.paginator import Paginator
import json
from .utils import create_paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

PAGE_SIZE=5

def index(request):
    if request.POST:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                url = reverse('LabControl.views.home')
                return HttpResponseRedirect(url)

        form = LoginForm(initial={'username': request.POST['username']})
        return render(request, 'LabControl/index.html', {'form': form, 'fail': True})
    else:
        form = LoginForm()
        return render(request,'LabControl/index.html', {'form': form})

@login_required()
def home(request):
    labs = Lab.objects.all()
    p = Paginator(labs,PAGE_SIZE)
    page_number = p.num_pages
    return render_to_response('LabControl/home.html',{'labs':p.page(1),
                                                      'page_number': page_number})

@login_required()
def query(request):
    query_form = QueryForm()
    try:
        labs = Lab.objects.filter(seccion=min(
            Lab.objects.order_by('seccion').values_list('seccion',flat=True).distinct()
        )).order_by('id')
        labs = {e.id:e.lab for e in labs }
    except Exception as e:
        labs = {}
    labs = {e.id:e.lab for e in labs }
    return render_to_response('LabControl/query.html', {'query_form': query_form,
                                                        'labs':labs})


@login_required()
def sub_query(request):
    query_form = QueryForm()
    try:
        labs = Lab.objects.filter(seccion=min(
            Lab.objects.order_by('seccion').values_list('seccion',flat=True).distinct()
        )).order_by('id')
        labs = {e.id:e.lab for e in labs }
    except Exception as e:
        labs = {}
    return render_to_response('LabControl/sub-query.html', {'query_form': query_form,
                                                        'labs':labs})



@login_required()
def add_lab(request):
    used_name = False
    invalid_date = False
    invalid_section = False
    success = False
    if request.POST:
        pattern = re.compile("\d{2,}/\d{1,2}/\d{4,}")
        lab = request.POST['lab']
        date = request.POST['date']
        seccion = request.POST['seccion']

        if not seccion.isdigit():
            invalid_section=True

        if pattern.match(date):
            day = date[0:date.index("/")]
            rest = date[date.index("/")+1:]
            month = rest[0:rest.index("/")]
            date = date[-4:] + '-' + month + '-' + day
        else:
            invalid_date=True

        old_lab = Lab.objects.filter(lab=lab,seccion=seccion)
        if old_lab:
             used_name = True

        if not invalid_date and not used_name and not invalid_section:
            new_lab = Lab(lab=lab,seccion=seccion,date=date)
            new_lab.save()
            success=True
    return render(request,'LabControl/add_lab.html',{'used_name': used_name,
                                                     'invalid_date': invalid_date,
                                                     'invalid_section':invalid_section,
                                                     'success':success})

@login_required()
def results(request):
    try:
        name = Lab.objects.all().order_by('id')[0].id
    except Exception as e:
        name =0
    try:
        seccion = Lab.objects.order_by('seccion').values_list('seccion',flat=True).distinct()[0]
    except Exception as e:
        seccion=0
    if request.GET:
        name = request.GET['name']
        seccion = request.GET['seccion']
        name = Lab.objects.get(seccion=seccion, lab=name).id

    seccion_select = ResultsForm()
    labs = Lab.objects.filter(seccion=seccion).order_by('id')
    labs = {e.id:e.lab for e in labs }

    try:
        lab = Lab.objects.get(id=name)
        response, page_number = create_paginator(lab, PAGE_SIZE,1)
    except Lab.DoesNotExist:
        response= {}
        page_number = 1
    return render(request,'LabControl/results.html',{'page_number': page_number,
                                                     'lab': name,
                                                     'seccion': seccion,
                                                     'seccion_select': seccion_select,
                                                     'table': json.dumps(response),
                                                     'first_seccion':json.dumps(labs)})


def registry(request):
    return JsonResponse({'OK': True})


@login_required()
def change_page(request):
    try:
        page_num = request.GET['page']
    except Exception as e:
        return HttpResponse('page not received', 500)
    labs = Lab.objects.all()
    p = Paginator(labs,PAGE_SIZE)
    response = {}

    for e in p.page(page_num):
        r = {'name': e.lab, 'seccion': e.seccion, 'date': e.date.strftime('%b %d, %Y')}
        response[e.id] = r
    return JsonResponse(response)

@login_required()
def change_page_results(request):
    try:
        page_num = request.GET['page']
        seccion= request.GET['seccion']
        lab = request.GET['lab']
        lab = Lab.objects.get(id=lab)
    except Exception as e:
        return HttpResponse('page not received', 500)

    response, _ = create_paginator(lab, PAGE_SIZE,page_num)

    return JsonResponse(response)

@login_required()
def get_labs_per_seccion(request):
    try:
        seccion = request.GET['seccion']
    except Exception as e:
        return HttpResponse('seccion not received',500)

    labs = Lab.objects.filter(seccion=seccion).order_by('id')
    first_lab = labs[0]
    response, page_number = create_paginator(first_lab,PAGE_SIZE,1)

    return JsonResponse({'labs': {e.id:e.lab for e in labs}, 'first_lab': response, 'page_number':page_number})

@login_required()
def get_table_for_lab(request):
    try:
        lab = request.GET['lab']
    except Exception as e:
        return HttpResponse('lab not received',500)

    lab = Lab.objects.get(id=lab)
    response, page_number = create_paginator(lab,PAGE_SIZE,1)

    return JsonResponse({'lab': response, 'page_number': page_number})

@login_required()
def teacher_logout(request):
    logout(request)
    url = reverse('LabControl.views.index')
    return HttpResponseRedirect(url)


def add_Teacher(request):
    user = User.objects.create_user('profesor', '', 'profesor')
    user.save()
    return HttpResponse(200)

@login_required()
def create_sub_query(request):
    name = request.POST['name']
    type = request.POST['type']
    query = json.loads(request.POST['query'])

    try:
        SubQuery.objects.get(name=name)
        return HttpResponse(content="SubQuery Already Exists", status=401)
    except SubQuery.DoesNotExist as e:
        try:
            SubQuery(name=name, json=query, type=type).save()
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse('SubQuery creation failed',status=501)


@login_required()
def get_all_subquery_names(request):
    names = {}
    i=1
    for sub_query in SubQuery.objects.all():
        i+=1
        names[i]=sub_query.name

    return JsonResponse(names)


@login_required()
def get_all_subquery(request):
    result = {}

    for sub_query in SubQuery.objects.all():
        result[sub_query.name]={'type': sub_query.type,
                                'query': sub_query.json}

    return JsonResponse(result)