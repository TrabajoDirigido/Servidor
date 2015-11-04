from ServerClient.views import connected_clients
from ServerClient.models import ClientInfo
__author__ = 'Camila Alvarez'

def parse_query(query,id): #debe retornar el id
    if not type(query) is dict:
        return (query,id)
    try:
        method = query['method']
        options ={
            'get': _get,
            'compare': _compare,
            'and': _and_operation,
            'or': _or_operation,
            'not_empty': _not_empty,
            'count': _count,
            'sort': _sort,
            'min': _min_operation,
            'max': _max_operation,
            'for': _for_operation,
            'alarm': _set_alarm
        }
        return options[method](query,id)
    except KeyError as e:
        return query


def _get(query,id):
    return ({'id':id,
             'method': 'get',
             'x': query['x'],
             'y': query['y'],
             'for': query['for'],
             'side': 'server'},id+1) if query['for'] == 'all' \
                                              or type(query['for']) is list \
        else ({'id':id,
               'method':'get',
               'x':query['x'],
               'y':query['y'],
               'for': query['for'],
               'side': 'client'+str(query['for'])},
               id+1)


def _compare(query, id):
    comp_id = id
    arg1, new_id = parse_query(query['arg1'],id)
    arg2, new_id = parse_query(query['arg2'],new_id)

    if not type(arg1) is dict and not type(arg2) is dict:
        side = 'client'
    elif not type(arg1) is dict:
        side = arg2['side']
    else:
        side = arg1['side']

    return ({'id':comp_id,
            'method': 'compare',
            'arg1': arg1,
            'arg2': arg2,
            'side': side}, new_id)


def _not_empty(query,id):
    return ({'id': id,
             'method': 'not_empty',
             'side': 'client',
             'x': query['x'],
             'y': query['y']},id+1)


def _count(query, id):
    return _list_value_operation(query,id,'count')


def _min_operation(query,id):
    return _list_value_operation(query,id,'min')


def _max_operation(query,id):
    return _list_value_operation(query,id,'max')


def _sort(query,id):
    return _list_value_operation(query,id,'sort')


def _vals_operations(query,id):
    if not type(query['vals']) is list:
        vals, new_id = parse_query(query['vals'], id+1)
    else:
        vals = []
        new_id = id+1

        for e in query['vals']:
            new_val, new_id = parse_query(e,new_id)
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

def _list_value_operation(query,id, method):
    vals, new_id = _vals_operations(query,id)
    return({'id':id,
            'method': method,
            'side': _get_list_side(vals),
            'vals': vals}, new_id)


def _logic_methods(query,id,method_type):
    vals, new_id = _vals_operations(query,id)

    return({'id':id,
            'method': 'logic',
            'side':_get_list_side(vals),
            'type': method_type,
            'vals': vals}, new_id)


def _and_operation(query, id):
    return _logic_methods(query,id,'and')


def _or_operation(query, id):
    return _logic_methods(query,id,'or')


def _for_operation(query,id):
    vals, new_id = _vals_operations(query,id)
    parsed_query, new_id = parse_query(query['query'], new_id)

    return({'id':id,
            'method':'for',
            'vals':vals,
            'side':_get_list_side(vals),
            'query':parsed_query}, new_id)


def _set_alarm(query,id):
    parsed_query, new_id = parse_query(query,id)
    return({'id': id,
            'method': 'alarm',
            'query': parsed_query,
            'side':'server',
            'time': query['time']}, new_id)

#---------------------------------------------------------------------------
def get_client_side_query(query):
    client_query_dict = {}
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
            'and': _vals_client,
            'or': _vals_client,
            'count': _vals_client,
            'sort': _vals_client,
            'min': _vals_client,
            'max': _vals_client,
            'for': _vals_client,
            'alarm': _set_alarm_client
        }
        return options[method](query,client_dict)
    except KeyError as e:
        return query


def _get_client(query, client_dict):
    client = query['for']
    new_query = {'id': query['id'],
                 'method': 'get',
                 'x': query['x'],
                 'y': query['y']}
    if client=='all':
        for ip in connected_clients:
            name = ClientInfo.objects.get(address=ip)
            client_dict[name] = new_query
    elif type(client) is list:
        for c in client:
            client_dict[c]=new_query
    else:
        client_dict[client]=new_query

    return



def _vals_client(query,client_dict):
    if query['side'][0:6]=='client':
        client_dict[_get_client_name(query)]=_format_query_to_client(query)
    else:
        if not type(query['vals']) is list:
            return _recursive_get_client_side_query(query['vals'], client_dict)
        for e in query['vals']:
            _recursive_get_client_side_query(e,client_dict)


def _compare_client(query, client_dict):

    if query['side'][0:6]=='client':
        client_dict[_get_client_name(query)]=_format_query_to_client(query)
    else:
        _recursive_get_client_side_query(query['arg1'],client_dict)
        _recursive_get_client_side_query(query['arg1'],client_dict)


def _set_alarm_client(query, client_dict):
    _recursive_get_client_side_query(query['query'],client_dict)


def _get_client_name(query):
    if not type(query) is dict:
        return
    try:
        method = query['method']
        options ={
            'get': _get_name,
            'compare': _compare_name,
            'and': _vals_name,
            'or': _vals_name,
            'count': _vals_name,
            'sort': _vals_name,
            'min': _vals_name,
            'max': _vals_name,
            'for': _for_operation_name
        }
        return options[method](query)
    except KeyError as e:
        return query


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
    name = _vals_name(query)
    if name is None:
        return _get_client_name(query['query'])
    return name

#---------------------------------------------------------------------

def _format_query_to_client(query):
    if not type(query) is dict:
        return {'var':query}
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
            'max': _vals_query_client,
            'for': _for_operation_query_client
        }
        return options[method](query)
    except KeyError as e:
        return query


def _get_query_client(query):
    return {'id': query['id'],
            'method': 'get',
            'x': query['x'],
            'y': query['y']}


def _compare_query_client(query):
    return {'id': query['id'],
            'method': 'compare',
            'arg1': _format_query_to_client(query['arg1']),
            'arg2': _format_query_to_client(query['arg2'])}


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


def _vals_query_client(query):
    vals = _obtain_vals_to_client(query)
    return {'id': query['id'],
            'method': query['method'],
            'vals': vals}

def _for_operation_query_client(query):
    vals = _obtain_vals_to_client(query)
    query = _format_query_to_client(query['query'])

    return {'id': query['id'],
            'method': 'for',
            'vals': vals,
            'query': query}