__author__ = 'Camila Alvarez'
import logging
from .models import ClientInfo

logger = logging.getLogger('error')

def get_client_side_query(query):
    client_query_dict = {}
    for c in ClientInfo.objects.all():
        client_query_dict[c.address]=[]
    _recursive_get_client_side_query(query,client_query_dict)

    return client_query_dict

def _recursive_get_client_side_query(query, client_dict):
    if not type(query) is dict:
        return
    try:
        method = query['method']
        options ={
            'get': _get_client,
            'compare': _compare_client,
            'logic': _vals_client,
            'count': _vals_client,
            'sort': _vals_client,
            'min': _vals_client,
            'max': _vals_client,
            'for': _vals_client,
            'alarm': _set_alarm_client,
            'filter': _vals_client,
            'dataChart': _data_chart_client,
            'existChart': _exist_chart_client
        }
        return options[method](query,client_dict)
    except KeyError as e:
        if 'type' in query:
            return
        logger.exception(Exception('Invalid query'))


def _data_chart_client(query, client_dict):
    client = query['for']
    new_query = _format_query_to_client({'id': query['id'],
                                        'method': 'dataChart',
                                        'type': query['type'],
                                        'sheet': query['sheet']})
    _set_client(client,client_dict,new_query)


def _set_client(client, client_dict,new_query):
    if client=='all':
        for ip in ClientInfo.objects.all():
            client_dict[ip.address].append(new_query)
    elif type(client) is list:
        for c in client:
            c = ClientInfo.objects.get(names=c)
            client_dict[c.address].append(new_query)
    else:
        c = ClientInfo.objects.get(names=client)
        client_dict[c.address].append(new_query)


def _exist_chart_client(query, client_dict):
    client = query['for']
    new_query = _format_query_to_client({'id': query['id'],
                                        'method': 'existChart',
                                        'sheet': query['sheet']})
    _set_client(client,client_dict,new_query)


def _get_client(query, client_dict):
    client = query['for']
    new_query = _format_query_to_client({'id': query['id'],
                                        'method': 'get',
                                        'sheet': query['sheet'],
                                        'x': query['x'],
                                        'y': query['y']})

    if 'type' in query:
        new_query['type'] = query['type']
    _set_client(client,client_dict,new_query)



def _vals_client(query,client_dict):
    if 'for' in query:
        r = dict(query)
        del r['for']
        _set_client(query['for'],client_dict, _format_query_to_client(r))
    else:
        if not type(query['vals']) is list:
            return _recursive_get_client_side_query(query['vals'], client_dict)
        for e in query['vals']:
            _recursive_get_client_side_query(e,client_dict)


def _compare_client(query, client_dict):
    if 'for' in query:
        r = dict(query)
        del r['for']
        _set_client(query['for'],client_dict, _format_query_to_client(r))
    else:
        _recursive_get_client_side_query(query['arg1'],client_dict)
        _recursive_get_client_side_query(query['arg2'],client_dict)


def _set_alarm_client(query, client_dict):
    _recursive_get_client_side_query(query['query'],client_dict)


# def _get_client_name(query):
#     if not type(query) is dict:
#         return
#     try:
#         method = query['method']
#         options ={
#             'get': _get_name,
#             'compare': _compare_name,
#             'logic': _vals_name,
#             'count': _vals_name,
#             'sort': _vals_name,
#             'min': _vals_name,
#             'max': _vals_name,
#             'for': _for_operation_name,
#             'filter': _vals_name
#         }
#         return options[method](query)
#     except KeyError as e:
#         logger.exception(Exception('Invalid query'))
#
# def _get_name(query):
#     return query['for']
#
#
# def _compare_name(query):
#     name = _get_client_name(query['arg1'])
#     if name is None:
#         name = _get_client_name(query['arg2'])
#     return name
#
#
# def _vals_name(query):
#     if not type(query['vals']) is list:
#         return _get_client_name(query['vals'])
#
#     for e in query['vals']:
#         name = _get_client_name(e)
#         if not name is None:
#             return name
#
# def _for_operation_name(query):
#     return _get_client_name(query['query'])

#---------------------------------------------------------------------

def _format_query_to_client(query):
    if not type(query) is dict:
        try:
            int(query)
            if type(query) is bool:
                query_type='bool'
            else:
                query_type='int'
        except ValueError:
            try:
                float(query)
                query_type='float'

            except ValueError:
                query_type='string'

        return {'var':query, 'type': query_type}
    try:
        method = query['method']
        options ={
            'get': _get_query_client,
            'compare': _compare_query_client,
            'logic': _logical_query_client,
            'count': _vals_query_client,
            'sort': _sort_client,
            'min': _vals_query_client,
            'max': _vals_query_client,
            'for': _for_operation_query_client,
            'filter': _filter_query_client,
            'dataChart': _data_chart_query_client,
            'existChart': _exist_chart_query_client
        }
        return options[method](query)
    except KeyError as e:
        if 'type' in query:
            return query
        raise Exception('Invalid query')


def _filter_query_client(query):
    vals = _obtain_vals_to_client(query)
    return {'id': query['id'],
            'method': 'filter',
            'type': query['type'],
            'var': query['var'],
            'vals': vals}

def _data_chart_query_client(query):
    new_query = {'id': query['id'],
                'method': 'dataChart',
                'sheet': query['sheet'],
                'type': query['type']}
    return new_query

def _exist_chart_query_client(query):
    new_query = {'id': query['id'],
                'method': 'existChart',
                'sheet': query['sheet']
                 }
    return new_query

def _get_query_client(query):
    new_query = {'id': query['id'],
            'method': 'get',
            'sheet': query['sheet'],
            'x': query['x'],
            'y': query['y']}
    if 'type' in query:
        new_query['type']=query['type']
    return new_query


def _compare_query_client(query):
    if not type(query['arg1']) is list:
        arg1 = _format_query_to_client(query['arg1'])
    else:
        arg1 = []
        for e in query['arg1']:
            arg1.append(_format_query_to_client(e))

    if not type(query['arg2']) is list:
        arg2 = _format_query_to_client(query['arg2'])
    else:
        arg2 = []
        for e in query['arg2']:
            arg2.append(_format_query_to_client(e))

    return {'id': query['id'],
            'method': 'compare',
            'arg1': arg1,
            'arg2': arg2}


def _obtain_vals_to_client(query):
    if not type(query['vals']) is list:
        vals = _format_query_to_client(query['vals'])
    else:
        vals = []
        for e in query['vals']:
            vals.append(_format_query_to_client(e))
    return vals


def _logical_query_client(query):
    vals = _obtain_vals_to_client(query)
    return {'id': query['id'],
            'method': 'logic',
            'type': query['type'],
            'vals': vals}


def _sort_client(query):
    new_query = _vals_query_client(query)
    return new_query


def _vals_query_client(query):
    vals = _obtain_vals_to_client(query)
    return {'id': query['id'],
            'method': query['method'],
            'vals': vals}

def _for_operation_query_client(query):
    vals = _obtain_vals_to_client(query)
    new_query = _format_query_to_client(query['query'])
    new_query['for_value'] = True

    return {'id': query['id'],
            'method': 'for',
            'vals': vals,
            'query': new_query}