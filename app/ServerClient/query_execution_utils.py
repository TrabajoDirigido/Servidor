import json
from .models import Result, Argument, Query
from functools import reduce
import copy
__author__ = 'Camila Alvarez'

def execute_query(query):
    query_text = eval(query.query)
    try:
        method=query_text['method']
        options={'compare': _execute_compare,
                 'logic': _execute_logic,
                 'count': _execute_count,
                 'sort': _execute_sort,
                 'min': _execute_min,
                 'max': _execute_max}
        return options[method](query)
    except KeyError:
        raise Exception('Invalid query')


def _execute_compare(query):
    if query.remaining_args != 0:
        for a in Query.objects.filter(parent=query.id):
            if a.remaining_args != 0:
                raise Exception("This query shouldn't be executing")
            execute_query(a)

    arg1 = []
    arg2 = []
    args = query.arguments.all()

    for a in args:
        if a.arg1:
            arg1.append(eval(a.value))
        else:
            arg2.append(eval(a.value))

    if len(arg1) != len(arg2):
        raise Exception('Invalid arguments')

    for i in range(0, len(arg1)):
        val = arg1[i] == arg2[i]
        result = Result(value=val, type='bool')
        result.save()
        query.results.add(result)
    query.remaining_results -= 1
    query.save()


def _execute_vals_function(query,f,type):
    if query.remaining_args != 0:
        for a in Query.objects.filter(parent=query.id):
            if a.remaining_args != 0:
                raise Exception("This query shouldn't be executing")
            execute_query(a)

    args = query.arguments.all()
    new_args =[]
    for a in args:
        new_args.append(eval(a.value))

    result = f(new_args) #Entrega una lista de resultados (aunque sea uno)
    for r in result:
        res = Result(value=r, type=type)
        res.save()
        query.results.add(res)
    query.remaining_results -= 1
    query.save()

def _check_bool_arg(args):
    for a in args:
        if not type(a) is bool:
            raise Exception('Wrong type argument')

def _execute_logic(query):
    query_type = eval(query.query)['type']
    return {'and': _execute_and,
            'or': _execute_or}[query_type](query)

def _execute_and(query):
    def _my_and(args):
        _check_bool_arg(args)
        return [reduce((lambda x,y : x and y), args, True)]
    return _execute_vals_function(query, _my_and, 'bool')


def _execute_or(query):
    def _my_or(args):
        _check_bool_arg(args)
        return [reduce((lambda x,y : x or y), args, False)]
    return _execute_vals_function(query, _my_or, 'bool')


def _execute_count(query):
    return _execute_vals_function(query, (lambda x: [len(x)]), 'int')


def _execute_sort(query):
    def _my_sort(reverse_value):
        def _inner_sort(args):
            args.sort(reverse=reverse_value)
            return args
        return _inner_sort

    query_text = eval(query.query)
    desc = True
    if 'des' in query_text:
        desc = query_text['des']
    arg1 = query.arguments.all()[0]
    return _execute_vals_function(query, _my_sort(desc), arg1.type)


def _execute_min(query):
    arg1 = query.arguments.all()[0]

    return _execute_vals_function(query, lambda x: [min(x)], arg1.type)


def _execute_max(query):
    arg1 = query.arguments.all()[0]
    return _execute_vals_function(query, lambda x: [max(x)], arg1.type)