__author__ = 'Camila Alvarez'
import logging

logger = logging.getLogger('error')

def get_client_side_query(query,clients):
    client_query_dict = {}
    for c in clients:
        client_query_dict[c]=[]
    _recursive_get_client_side_query(query,client_query_dict,clients)

    return client_query_dict

def _recursive_get_client_side_query(query, client_dict,clients):
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
            'filter': _vals_client
        }
        return options[method](query,client_dict,clients)
    except KeyError as e:
        logger.exception(Exception('Invalid query'))


def _get_client(query, client_dict,clients):
    client = query['for']
    new_query = _format_query_to_client({'id': query['id'],
                                        'method': 'get',
                                        'type': query['type'],
                                        'sheet': query['sheet'],
                                        'x': query['x'],
                                        'y': query['y']})
    if client=='all':
        for ip in clients:
            client_dict[ip].append(new_query)
    elif type(client) is list:
        for c in client:
            client_dict[c].append(new_query)
    else:
        client_dict[client].append(new_query)

    return

def _assign_query_to_client(query, client_dict):
    client = _get_client_name(query)
    if client in client_dict:
        client_dict[_get_client_name(query)].append(_format_query_to_client(query))

def _vals_client(query,client_dict,clients):
    if query['side'][0:6]=='client':
        _assign_query_to_client(query,client_dict)
        #client_dict[_get_client_name(query)].append(_format_query_to_client(query))
    else:
        if not type(query['vals']) is list:
            return _recursive_get_client_side_query(query['vals'], client_dict,clients)
        for e in query['vals']:
            _recursive_get_client_side_query(e,client_dict,clients)


def _compare_client(query, client_dict,clients):

    if query['side'][0:6]=='client':
        _assign_query_to_client(query,client_dict)
        #client_dict[_get_client_name(query)].append(_format_query_to_client(query))
    else:
        _recursive_get_client_side_query(query['arg1'],client_dict,clients)
        _recursive_get_client_side_query(query['arg2'],client_dict,clients)


def _set_alarm_client(query, client_dict,clients):
    _recursive_get_client_side_query(query['query'],client_dict,clients)


def _get_client_name(query):
    if not type(query) is dict:
        return
    try:
        method = query['method']
        options ={
            'get': _get_name,
            'compare': _compare_name,
            'logic': _vals_name,
            'count': _vals_name,
            'sort': _vals_name,
            'min': _vals_name,
            'max': _vals_name,
            'for': _for_operation_name,
            'filter': _vals_name
        }
        return options[method](query)
    except KeyError as e:
        logger.exception(Exception('Invalid query'))

def _get_name(query):
    return query['for']


def _compare_name(query):
    name = _get_client_name(query['arg1'])
    if name is None:
        name = _get_client_name(query['arg2'])
    return name


def _vals_name(query):
    if not type(query['vals']) is list:
        return _get_client_name(query['vals'])

    for e in query['vals']:
        name = _get_client_name(e)
        if not name is None:
            return name

def _for_operation_name(query):
    return _get_client_name(query['query'])

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
            'filter': _filter_query_client
        }
        return options[method](query)
    except KeyError as e:
        raise Exception('Invalid query')


def _filter_query_client(query):
    vals = _obtain_vals_to_client(query)
    new_filter = query['filter']
    return {'id': query['id'],
            'method': 'filter',
            'filter': {'type': new_filter['type'], 'var': _format_query_to_client(new_filter['var'])},
            'vals': vals}

def _get_query_client(query):

    return {'id': query['id'],
            'method': 'get',
            'type': query['type'],
            'sheet': _format_query_to_client(query['sheet']),
            'x': query['x'],
            'y': query['y']}


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
    if 'des' in query:
        new_query['des']= {'var': query['des'], 'type': 'bool'}
    else:
        new_query['des']={'var': True, 'type': 'bool'}
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