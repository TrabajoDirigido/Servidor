__author__ = 'Camila Alvarez'
import logging

logger = logging.getLogger('error')
def replace_for_value(for_value, vals):
    if not type(vals) is list:
       return _replace_for_value(vals, for_value)
    else:
        new_vals=[]
        for e in vals:
            new_vals.append(_replace_for_value(e, for_value))
        return new_vals

#Por ahora no hay for dentro de for
def _replace_for_value(query, for_value):
    if query=='for_value':
        return for_value
    if not type(query) is dict:
        return query
    try:
        method = query['method']
        options ={
            'get': _get_query_client,
            'compare': _compare_query_client,
            'and': _logical_query_client,
            'or': _logical_query_client,
            'count': _vals_query_client,
            'sort': _vals_query_client,
            'min': _vals_query_client,
            'max': _vals_query_client
        }
        return options[method](query,for_value)
    except KeyError as e:
        logger.exception(Exception('Invalid query'))



def _get_query_client(query,for_value):
    return {'method': 'get',
            'x': _replace_for_value(query['x'], for_value),
            'y': _replace_for_value(query['y'], for_value)}


def _compare_query_client(query,for_value):
    return {'method': 'compare',
            'arg1': _replace_for_value(query['arg1'],for_value),
            'arg2': _replace_for_value(query['arg2'],for_value)}


def _obtain_vals_for(query,for_value):
    if not type(query['vals']) is list:
        vals = _replace_for_value(query['vals'],for_value)
    else:
        vals = []
        for e in query['vals']:
            vals.append(_replace_for_value(e,for_value))
    return vals


def _logical_query_client(query,for_value):
    vals = _obtain_vals_for(query,for_value)
    return {'method': 'logic',
            'type': query['type'],
            'vals': vals}


def _vals_query_client(query,for_value):
    vals = _obtain_vals_for(query,for_value)
    return {'method': query['method'],
            'vals': vals}

def _for_operation_query_client(query,for_value):
    vals = _obtain_vals_for(query,for_value)
    new_query = _replace_for_value(query['query'],for_value)

    return {'method': 'for',
            'vals': vals,
            'query': new_query}