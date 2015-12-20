from .models import Query, Lab, Result,Argument, ClientInfo
import logging
from .query_execution_utils import execute_query
__author__ = 'Camila Alvarez'

logger = logging.getLogger('error')
def _get_type(query):
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
    return query_type


def save_parsed_query_to_database(query,clients,lab):
    _save_recursive(query,-1,clients, True,lab)

def _save_recursive(query,parent,clients, arg1,lab):
    if not type(query) is dict:
        my_type = _get_type(query)
        parent_obj = Query.objects.get(id=parent)
        parent_obj.remaining_args -= 1
        arg = Argument(value=query, type=my_type, arg1=arg1, query=parent_obj)
        arg.save()
        parent_obj.save()
        return

    try:
        method = query['method']
        options ={
            'get': _save_get,
            'compare': _save_compare,
            'logic': _save_vals_operation,
            'not_empty': _save_not_empty,
            'count': _save_vals_operation,
            'sort': _save_vals_operation,
            'min': _save_vals_operation,
            'max': _save_vals_operation,
            'for': _save_vals_operation,
            'alarm': _save_set_alarm,
            'filter': _save_vals_operation
        }
        return options[method](query,parent,clients, arg1,lab)
    except KeyError as e:
        if 'type' in query:
            my_type = query['type']
            value = query['var']
            parent_obj = Query.objects.get(id=parent)
            parent_obj.remaining_args -= 1
            arg = Argument(value=value, type=my_type, arg1=arg1, query=parent_obj)
            arg.save()
            parent_obj.save()
            return
        logger.exception(Exception('Invalid query'))


def _save_query(query,parent,remaining_results, remaining_args, arg1,lab):
    try:
        lab = Lab.objects.get(id=lab)
    except Lab.DoesNotExist:
        logger.exception(Exception("Lab does not exist"))
    try:
        q = Query(id=query['id'], lab=lab,query=query, parent=parent,
                  remaining_results=remaining_results, remaining_args=remaining_args,
                  arg1=arg1,name=query['AS'])
        q.save()
    except Exception as e:
        logger.exception(Exception("Couldn't save query"))


def _execute_if_posible(query):
    q = Query.objects.get(id=query['id'])
    if q.remaining_args == 0:
        execute_query(q)
        if q.parent != -1:
            parent_obj = Query.objects.get(id=q.parent)
            parent_obj.remaining_args -= 1
            for r in Result.objects.filter(query=q):
                arg = Argument(value=r.value, type=r.type, arg1=q.arg1, query=parent_obj)
                arg.save()
            parent_obj.save()
            q.delete()


def _save_get(query,parent,clients, arg1,lab):
    query_for = query['for']
    if type(query_for) is list:
        remaining_results = len(query_for)
    elif query_for == 'all':
        remaining_results = len(clients)
    else:
        remaining_results=1
    _save_query(query,parent,remaining_results, 0, arg1,lab)


def _save_list_arg(arg,parent,clients, arg1,lab):
    if type(arg) is list:
        for e in arg:
            _save_recursive(e,parent,clients,arg1,lab)
    else:
        _save_recursive(arg,parent,clients,arg1,lab)


def _save_compare(query,parent,clients,arg1,lab):
    remaining_results = 1
    remaining_args1 = len(query['arg1']) if type(query['arg1']) is list else 1
    remaining_args2 = len(query['arg2']) if type(query['arg2']) is list else 1
    remaining_args = remaining_args1 + remaining_args2
    if 'for' in query:
        remaining_args=0
        if type(query['for']) is list:
            remaining_results = len(query['for'])
        elif query['for'] == 'all':
            remaining_results = len(clients)
        else:
            remaining_results=1
    _save_query(query,parent,remaining_results,remaining_args, arg1,lab)

    if 'for' not in query:
        _save_list_arg(query['arg1'], query['id'], clients, True,lab)
        _save_list_arg(query['arg2'], query['id'], clients, False,lab)
        _execute_if_posible(query)


def _save_vals_operation(query, parent, clients, arg1,lab):
    remaining_results = 1
    remaining_args = len(query['vals']) if type(query['vals']) is list else 1
    if 'for' in query:
        remaining_args = 0
        if type(query['for']) is list:
            remaining_results = len(query['for'])
        elif query['for'] == 'all':
            remaining_results = len(clients)
        else:
            remaining_results=1
    _save_query(query,parent, remaining_results,remaining_args , arg1,lab)
    if 'for' not in query:
        _save_list_arg(query['vals'],query['id'],clients, arg1,lab)
        _execute_if_posible(query)


def _save_not_empty(query,parent,clients, arg1,lab):
    _save_query(query,parent,1,0, arg1,lab)


def _save_set_alarm(query,parent,clients, arg1,lab):
    _save_query(query,parent,1,1, arg1,lab)
    _save_recursive(query['query'], query['id'],clients, arg1,lab)
    _execute_if_posible(query)



def save_result(id, result,origin):
    try:
        query = Query.objects.get(id=id)
        for res in result:
            type = res['type']
            if type == 'null':
                value = None
            else:
                value = res['var']
            result = Result(value=value, type=type, origin=origin, query=query)
            result.save()
        query.remaining_results -= 1
        query.save()
        if query.remaining_results == 0:
            _update_results(query)
    except Query.DoesNotExist:
        logger.exception(Exception('invalid Query'))


def _update_results(query):
    query_text = eval(query.query)
    while (query.remaining_args == 0 or query_text['method'] == 'get'):
        #procesar query
        if query_text['method'] != 'get':
            execute_query(query)

        if query.parent == -1:
            break

        old_query = query
        parent = old_query.parent
        query = Query.objects.get(id=parent)
        res = Result.objects.filter(query=old_query)

        for r in res:
            new_arg = Argument(value=r.value, type= r.type, arg1=old_query.arg1, query=query, origin=r.origin)
            new_arg.save()
        query.remaining_args -= 1
        query.save()
        old_query.delete()
        query_text = eval(query.query)


