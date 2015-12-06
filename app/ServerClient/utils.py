from .utils_for import replace_for_value
from .query_execution_utils import execute_query
from .models import Query
import logging
__author__ = 'Camila Alvarez'

logger = logging.getLogger('error')


def parse_query(query,id,clients): #debe retornar el id
    if not type(query) is dict:
        return (query, id)
    try:
        method = query['method']
        options ={
            'get': _get,
            'compare': _compare,
            'logic': _logic_operation,
            'not_empty': _not_empty,
            'count': _count,
            'sort': _sort,
            'min': _min_operation,
            'max': _max_operation,
            'for': _for_operation,
            'alarm': _set_alarm,
            'filter': _filter
        }
        return options[method](query,id,clients)
    except KeyError as e:
        if 'type'in query:
            return (query, id)
        logger.error(Exception('Invalid Query'))


def _filter(query, id, clients):
    vals, new_id = _vals_operations(query,id,clients)
    new_query = {'id': id,
                'method': 'filter',
                'vals': vals,
                'AS': query['AS'] if 'AS' in query else 'filter'+str(id),
                'type': query['type'],
                'var': query['var']}
    if 'for' in query:
        new_query['for']=query['for']
    return new_query, new_id



def _get(query,id,clients):
    new_query = {'id': id,
                 'method': 'get',
                 'x': query['x'],
                 'y': query['y'],
                 'AS': query['AS'] if 'AS' in query else 'get'+str(id),
                 'sheet': query['sheet'] if 'sheet' in query else [1]}
    if 'type' in query:
        new_query['type']=query['type']
    if 'for' in query:
        new_query['for']=query['for']

    return new_query, id+1

def _parse_args(query,id,clients):
    if type(query) is list:
        res = []
        new_id = id
        for e in query:
            arg1, new_id = parse_query(e, new_id, clients)
            res.append(arg1)
    else:
        res, new_id = parse_query(query, id, clients)
    return res, new_id

def _compare(query, id,clients):
    comp_id = id
    arg1, new_id = _parse_args(query['arg1'],id+1,clients)
    arg2, new_id = _parse_args(query['arg2'],new_id,clients)
    new_query = {'id':comp_id,
                'method': 'compare',
                'arg1': arg1,
                'arg2': arg2,
                'AS': query['AS'] if 'AS' in query else 'compare'+str(comp_id)}
    if 'for' in query:
        new_query['for']=query['for']

    return (new_query, new_id)


def _not_empty(query,id,clients):
    return ({'id': id,
             'method': 'not_empty',
             'for': 'all',
             'AS': query['AS'] if 'AS' in query else 'not_empty'+str(id),
             'x': query['x'],
             'y': query['y']},id+1)


def _count(query, id,clients):
    return _list_value_operation(query,id,'count',clients)


def _min_operation(query,id,clients):
    return _list_value_operation(query,id,'min',clients)


def _max_operation(query,id,clients):
    return _list_value_operation(query,id,'max',clients)


def _sort(query,id,clients):
    new_query, new_id = _list_value_operation(query,id,'sort',clients)
    if 'des' in query:
        new_query['des']= query['des']
    else:
        new_query['des']=True
    return new_query,new_id


def _vals_operations(query,id,clients):
    if not type(query['vals']) is list:
        vals, new_id = parse_query(query['vals'], id+1,clients)
    else:
        vals = []
        new_id = id+1

        for e in query['vals']:
            new_val, new_id = parse_query(e,new_id,clients)
            vals.append(new_val)
    return vals, new_id


def _get_list_side(vals):
    side=""
    if type(vals) is list:
        for e in vals:
            if side=='server':
                break
            if not type(e) is dict:
                side='client'
            else:
                if side!="":
                    side=e['side'] if e['side']==side else 'server'
                else:
                    side=e['side']
    else:
        if type(vals) is dict:
            if side!="":
                side=vals['side'] if vals['side']==side else 'server'
            else:
                side=vals['side']
        else:
            side='client'
    return side

def _list_value_operation(query,id, method,clients):
    vals, new_id = _vals_operations(query,id,clients)
    new_query = {'id':id,
                'method': method,
                'AS': query['AS'] if 'AS' in query else method+str(id),
                'vals': vals}
    if 'for' in query:
        new_query['for']=query['for']
    return(new_query, new_id)


def _logic_methods(query,id,method_type,clients):
    vals, new_id = _vals_operations(query,id,clients)
    new_query = {'id':id,
                'method': 'logic',
                'AS': query['AS'] if 'AS' in query else method_type+str(id),
                'type': method_type,
                'vals': vals}
    if 'for' in query:
        new_query['for']=query['for']
    return(new_query, new_id)


def _logic_operation(query,id,clients):
    return _logic_methods(query,id, query['type'],clients)


def _for_operation(query,id,clients):
    vals = replace_for_value(query['for_value'],query['vals'])
    parsed_query, new_id = parse_query(query['query'], id+1,clients)

    return({'id':id,
            'method':'for',
            'vals':vals,
            'AS': query['AS'] if 'AS' in query else 'for'+str(id),
            'query':parsed_query}, new_id)


def _set_alarm(query,id,clients):
    parsed_query, new_id = parse_query(query,id,clients)
    return({'id': id,
            'method': 'alarm',
            'query': parsed_query,
            'AS': query['AS'] if 'AS' in query else 'alarm'+str(id),
            'time': query['time']}, new_id)

#---------------------------------------------------------------------------
