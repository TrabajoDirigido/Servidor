from ServerClient.models import Query,Result, ClientInfo, Lab
from django.core.paginator import Paginator

__author__ = 'Camila Alvarez'

def new_choices():
    try:
        choices = []
        for e in Lab.objects.all():
            if e.seccion not in choices:
                choices.append(e.seccion)
        choices.sort()
        new_choices = []
        for e in choices:
            new_choices.append((e,e))
    except Exception as e:
        print(e)
        new_choices = []

    print(new_choices)
    return new_choices

def create_paginator(lab, page_size,page):
    query = Query.objects.filter(parent=-1, lab=lab)

    p = Paginator(query,page_size)
    response = {}
    for e in p.page(page):
        res = {}
        for result in Result.objects.filter(query=e):
            try:
                names = ClientInfo.objects.get(address=result.origin).names
            except Exception:
                names = result.origin
            if names not in res:
                res[names] = []
            res[names].append(result.value)

        final_result = ""
        if len(res)==1 and 'localhost' in res:
            final_result = '['+ ', '.join(res['localhost'])+']'
        elif len(res)>=1:
            for resp in res:
                final_result += resp+': '+'['+ ', '.join(res[resp])+']<br>'
            final_result = final_result[:-4]

        r = {'name': e.name, 'value': final_result}
        response[e.id] = r


    page_number = p.num_pages

    return response,page_number