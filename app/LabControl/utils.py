from ServerClient.models import Query,Result
from django.core.paginator import Paginator

__author__ = 'Camila Alvarez'


def create_paginator(lab, page_size,page):
    query = Query.objects.filter(parent=-1, lab=lab)

    p = Paginator(query,page_size)
    response = {}

    for e in p.page(page):
        res = Result.objects.filter(query=e).values_list('value',flat=True)
        res = '['+ ', '.join(res)+']'
        r = {'name': e.name, 'value': res}
        response[e.id] = r

    page_number = p.num_pages

    return response,page_number