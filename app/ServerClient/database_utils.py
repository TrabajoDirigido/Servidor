from .models import Query, Lab, Result,Argument
import datetime
import json
from .query_execution_utils import execute_query
__author__ = 'Camila Alvarez'


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


def save_parsed_query_to_database(query,clients):
    _save_recursive(query,-1,clients, True)

def _save_recursive(query,parent,clients, arg1):
    if not type(query) is dict:
        my_type = _get_type(query)
        parent_obj = Query.objects.get(id=parent)
        parent_obj.remaining_args -= 1
        arg = Argument(value=query, type=my_type, arg1=arg1)
        arg.save()
        parent_obj.arguments.add(arg)
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
            'alarm': _save_set_alarm
        }
        return options[method](query,parent,clients, arg1)
    except KeyError as e:
        raise Exception('Invalid query')


def _save_query(query,parent,remaining_results, remaining_args, arg1):
    date = str(datetime.date.today())
    try:
        lab = Lab.objects.get(date=date)
    except Lab.DoesNotExist:
        lab = Lab(lab="Lab 1")
        lab.save()
        #raise Exception("Lab does not exist")
    try:
        q = Query(id=query['id'], lab=lab,query=query, parent=parent,
                  remaining_results=remaining_results, remaining_args=remaining_args,
                  arg1=arg1)
        q.save()
    except Exception as e:
        raise Exception("Couldn't save query")


def _execute_if_posible(query):
    q = Query.objects.get(id=query['id'])
    if q.remaining_args == 0:
        execute_query(q)
        if q.parent!=-1:
            parent_obj = Query.objects.get(id=q.parent)
            parent_obj.remaining_args -= 1
            for r in q.results.all():
                arg = Argument(value=r.value, type=r.type, arg1=q.arg1)
                arg.save()
                parent_obj.arguments.add(arg)
            parent_obj.save()


def _save_get(query,parent,clients, arg1):
    query_for = query['for']
    if type(query_for) is list:
        remaining_results = len(query_for)
    elif query_for == 'all':
        remaining_results = len(clients)
    else:
        remaining_results=1
    _save_query(query,parent,remaining_results,0, arg1)


def _save_list_arg(arg,parent,clients, arg1):
    if type(arg) is list:
        for e in arg:
            _save_recursive(e,parent,clients,arg1)
    else:
        _save_recursive(arg,parent,clients,arg1)


def _save_compare(query,parent,clients,arg1):
    remaining_args1 = len(query['arg1']) if type(query['arg1']) is list else 1
    remaining_args2 = len(query['arg2']) if type(query['arg2']) is list else 1
    _save_query(query,parent,1,remaining_args1+remaining_args2, arg1)
    _save_list_arg(query['arg1'], query['id'], clients, True)
    _save_list_arg(query['arg2'], query['id'], clients, False)
    _execute_if_posible(query)


def _save_vals_operation(query, parent, clients, arg1):
    _save_query(query,parent, 1, len(query['vals']) if type(query['vals']) is list else 1, True)
    _save_list_arg(query['vals'],query['id'],clients, arg1)
    _execute_if_posible(query)


def _save_not_empty(query,parent,clients, arg1):
    _save_query(query,parent,1,0, arg1)


def _save_set_alarm(query,parent,clients, arg1):
    _save_query(query,parent,1,1, arg1)
    _save_recursive(query['query'], query['id'],clients, arg1)
    _execute_if_posible(query)



def save_result(id, result):
    try:
        query = Query.objects.get(id=id)
        for res in result:
            value = res['val']
            type = res['type']
            result = Result(value=value, type=type)
            result.save()
            query.results.add(result)
            query.save()

        query.remaining_results -= 1

        if query.remaining_results == 0:
            _update_results(query)
    except Query.DoesNotExist:
        raise Exception('invalid Query')


def _update_results(query):
    while query.remaining_args == 0 and query.parent != -1:
        query_text = eval(query.query)

        #procesar query
        if query_text['method'] != 'get':
            execute_query(query)

        old_query = query
        parent = old_query.parent
        query = Query.objects.get(id=parent)
        res = old_query.results.all()
        arg_id = query.remaining_args

        for r in res:
            new_arg = Argument(value=r.value, type= r.type, arg1=old_query.arg1)
            new_arg.save()
            query.arguments.add(new_arg)
        query.save()
        query.remaining_args -= 1


