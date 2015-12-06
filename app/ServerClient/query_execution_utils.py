import json
from .models import Result, Argument, Query
from functools import reduce
import copy
import logging
__author__ = 'Camila Alvarez'

logger = logging.getLogger('error')
def execute_query(query):
    query_text = eval(query.query)
    try:
        method=query_text['method']
        options={'compare': _execute_compare,
                 'logic': _execute_logic,
                 'count': _execute_count,
                 'sort': _execute_sort,
                 'min': _execute_min,
                 'max': _execute_max,
                 'filter': _execute_filter
                 }
        return options[method](query)
    except KeyError:
        logger.exception(Exception('Invalid query'))


def _execute_for_one_longer_list(query,long_arg,short_arg):
    for i in range(0, len(long_arg)):
        val = short_arg == long_arg[i]
        result = Result(value=val, type='bool', query=query)
        result.save()
    query.remaining_results -= 1
    query.save()


def _execute_compare(query):
    if query.remaining_args != 0:
        for a in Query.objects.filter(parent=query.id):
            if a.remaining_args != 0:
                logger.exception(Exception("This query shouldn't be executing"))
                return

            execute_query(a)

    arg1 = []
    arg2 = []
    args = Argument.objects.filter(query=query)

    for a in args:
        if a.arg1:
            try:
                arg1.append(eval(a.value))
            except Exception:
                arg1.append(a.value)
        else:
            try:
                arg2.append(eval(a.value))
            except Exception:
                arg2.append(a.value)

    if len(arg1) != len(arg2) and len(arg1)!=1 and len(arg2)!=1:
        logger.exception(Exception('Invalid arguments'))
        return

    if len(arg1)==1:
        _execute_for_one_longer_list(query,arg2,arg1[0])
    elif len(arg2)==1:
        _execute_for_one_longer_list(query,arg1,arg2[0])
    else:
        for i in range(0, len(arg1)):
            val = arg1[i] == arg2[i]
            result = Result(value=val, type='bool', query=query)
            result.save()
        query.remaining_results -= 1
        query.save()



def _execute_vals_function(query,f,type):
    if query.remaining_args != 0:
        for a in Query.objects.filter(parent=query.id):
            if a.remaining_args != 0:
                logger.exception(Exception("This query shouldn't be executing"))
                return
            execute_query(a)

    args = Argument.objects.filter(query=query)
    new_args =[]
    for a in args:
        try:
            new_args.append(eval(a.value))
        except Exception:
            new_args.append(a.value)


    result = f(new_args) #Entrega una lista de resultados (aunque sea uno)
    for r in result:
        res = Result(value=r, type=type, query=query)
        res.save()
    query.remaining_results -= 1
    query.save()

def _check_bool_arg(args):
    for a in args:
        if not type(a) is bool:
            logger.exception(Exception('Wrong type argument'))
            return

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

def _execute_filter(query):
    def _my_filter():
        query_text = eval(query.query)
        value = query_text['var']['var']
        type = query_text['var']['type']
        # value ={'int': int(value),
        #         'float': float(value),
        #         'string': str(value),
        #         'bool': bool(value)}[type]
        method = query_text['type']
        def _inside_filter(args):
            return list(filter({
                            'equal': lambda compare_value:  value == compare_value,
                            'not_equal': lambda compare_value: value != compare_value
                            }[method],
                          args))
        return _inside_filter

    return _execute_vals_function(query, _my_filter(), 'int')


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
        desc = query_text['des']['var']
    arg1 = Argument.objects.filter(query=query)[0]
    return _execute_vals_function(query, _my_sort(desc), arg1.type)


def _execute_min(query):
    arg1 = Argument.objects.filter(query=query)[0]

    return _execute_vals_function(query, lambda x: [min(x)], arg1.type)


def _execute_max(query):
    arg1 = Argument.objects.filter(query=query)[0]
    return _execute_vals_function(query, lambda x: [max(x)], arg1.type)