from .utils_for import replace_for_value
from .query_execution_utils import execute_query
from .models import Query
__author__ = 'Camila Alvarez'

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
            'alarm': _set_alarm
        }
        return options[method](query,id,clients)
    except KeyError as e:
        raise Exception('Invalid query')


def _get(query,id,clients):

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


def _not_empty(query,id,clients):
    return ({'id': id,
             'method': 'not_empty',
             'side': 'client',
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
    if 'desc' in query:
        new_query['desc']=query['desc']
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
    return({'id':id,
            'method': method,
            'side': _get_list_side(vals),
            'vals': vals}, new_id)


def _logic_methods(query,id,method_type,clients):
    vals, new_id = _vals_operations(query,id,clients)

    return({'id':id,
            'method': 'logic',
            'side':_get_list_side(vals),
            'type': method_type,
            'vals': vals}, new_id)


def _logic_operation(query,id,clients):
    return _logic_methods(query,id, query['type'],clients)


def _for_operation(query,id,clients):
    #vals, new_id = _vals_operations(query,id,clients)
    vals = replace_for_value(query['for_value'],query['vals'])
    parsed_query, new_id = parse_query(query['query'], id+1,clients)

    return({'id':id,
            'method':'for',
            'vals':vals,
            'side':parsed_query['side'],#_get_list_side(vals),
            'query':parsed_query}, new_id)


def _set_alarm(query,id,clients):
    parsed_query, new_id = parse_query(query,id,clients)
    return({'id': id,
            'method': 'alarm',
            'query': parsed_query,
            'side':'server',
            'time': query['time']}, new_id)

#---------------------------------------------------------------------------
def get_client_side_query(query,clients):
    client_query_dict = {}
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
            'alarm': _set_alarm_client
        }
        return options[method](query,client_dict,clients)
    except KeyError as e:
        raise Exception('Invalid query')


def _get_client(query, client_dict,clients):
    client = query['for']
    new_query = _format_query_to_client({'id': query['id'],
                                        'method': 'get',
                                        'x': query['x'],
                                        'y': query['y']})
    if client=='all':
        for ip in clients:
            client_dict[ip] = new_query
    elif type(client) is list:
        for c in client:
            client_dict[c]=new_query
    else:
        client_dict[client]=new_query

    return



def _vals_client(query,client_dict,clients):
    if query['side'][0:6]=='client':
        client_dict[_get_client_name(query)]=_format_query_to_client(query)
    else:
        if not type(query['vals']) is list:
            return _recursive_get_client_side_query(query['vals'], client_dict,clients)
        for e in query['vals']:
            _recursive_get_client_side_query(e,client_dict,clients)


def _compare_client(query, client_dict,clients):

    if query['side'][0:6]=='client':
        client_dict[_get_client_name(query)]=_format_query_to_client(query)
    else:
        _recursive_get_client_side_query(query['arg1'],client_dict,clients)
        _recursive_get_client_side_query(query['arg1'],client_dict,clients)


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
            'for': _for_operation_name
        }
        return options[method](query)
    except KeyError as e:
        raise Exception('Invalid query')


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
    #name = _vals_name(query)
    #if name is None:
    return _get_client_name(query['query'])
    #return name

#---------------------------------------------------------------------

def _format_query_to_client(query):
    if not type(query) is dict:
        try:
            int(query)
            query_type='int'
        except ValueError:
            try:
                float(query)
                query_type='float'

            except ValueError:
                try:
                    bool(query)
                    query_type='bool'

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
            'for': _for_operation_query_client
        }
        return options[method](query)
    except KeyError as e:
        raise Exception('Invalid query')


def _get_query_client(query):
    parsed_x = []
    parsed_y = []
    if type(query['x']) is list:
        for val_x in query['x']:
            parsed_x.append(_format_query_to_client(val_x))

    for val_y in query['y']:
        parsed_y.append(_format_query_to_client(val_y))

    return {'id': query['id'],
            'method': 'get',
            'x': parsed_y,
            'y': parsed_x}


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
    if 'desc' in query:
        new_query['desc']= query['desc']
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