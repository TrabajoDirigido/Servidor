/**
 * Created by Camila Alvarez on 20-11-2015.
 */

var server_options = ['SERVER_GET', 'SERVER_FILTER', 'SERVER_COUNT', 'SERVER_MIN', 'SERVER_MAX'];
var server_get_array = ['GET', 'COUNT', 'AND','OR', 'MIN', 'MAX'];
var server_filter = ['SERVER_FILTER_BOOL', 'SERVER_FILTER_NUMERIC'];
var server_filter_bool_cond = ['EQUAL_TRUE', 'EQUAL_FALSE'];
var server_filter_bool = ['AND', 'OR'];

var server_filter_num_cond =  ['CONDITION_EQUAL', 'CONDITION_NOT_EQUAL'];
var server_filter_num = ['COUNT', 'MIN', 'MAX'];
var server_count = ['SERVER_FILTER'];
var server_min_max = ['SERVER_FILTER_NUMERIC', 'COUNT', 'MIN', 'MAX'];

var options = ['GET', 'COUNT', 'AND','OR', 'MIN', 'MAX'];

var get_array = ['GET_COMPARABLE', 'GET_OBJECT'];
var get_comparable_array = ['GET_NUMERIC', 'GET_BOOLEAN', 'GET_FORMULA', 'GET_STRING'];

var count_array = ['FILTER'];
var or_and_array = ['AND|OR', 'EQUAL'];

var equal_array = ['GET', 'VAR', 'SORT','EQUAL','FILTER'];
var sort_array = ['GET_COMPARABLE', 'FILTER_COMPARABLE', 'EQUAL'];

var filter_array = ['FILTER_OBJECT', 'FILTER_COMPARABLE'];
var filter_object_array = ['GET_OBJECT'];
var filter_comparable_array = ['GET_COMPARABLE', 'EQUAL', 'SORT'];
var conditions_array = server_filter_num_cond;
var order_array = ['ASCENDENTE', 'DESCENDENTE'];
var vars = ['NUMERIC', 'STRING', 'BOOLEAN'];

var and_or = ['AND', 'OR'];

var query_dict = {
    'GET': [get_array], 'GET_COMPARABLE': [get_comparable_array],
    'COUNT': [count_array], 'OR': [or_and_array], 'AND': [or_and_array], 'EQUAL': [equal_array,equal_array],
    'SORT': [order_array,sort_array], 'FILTER': [filter_array], 'FILTER_OBJECT': [conditions_array,filter_object_array],
    'FILTER_COMPARABLE': [conditions_array,filter_comparable_array], 'VAR': [vars], 'COMPARE':[equal_array],
    'MIN':[sort_array], 'MAX':[sort_array], 'SERVER_FILTER_NUMERIC': [server_filter_num_cond, server_filter_num],
    'SERVER_FILTER_BOOL': [server_filter_bool_cond, server_filter_bool], 'SERVER_GET': [server_get_array],
    'SERVER_FILTER': [server_filter], 'SERVER_COUNT': [server_count], 'SERVER_MIN': [server_min_max],
    'SERVER_MAX': [server_min_max]
};

var objetivo = ['OBJETIVO:'];
var get_arg = ['HOJA:', 'Y: ', 'X: ' ];
var var_arg = ['VALOR: '];
var list_arg = ['ARGUMENTOS:   ['];
var equal_arg = ['ARG1:   [', 'ARG2:   ['];
var sort_arg = ['ORDENAR:   [', 'ARGUMENTOS:   ['];
var filter_arg = ['FILTRO:   [', 'ARGUMENTOS:   ['];


var argument_dict = {
    'GET_NUMERIC': get_arg, 'GET_BOOLEAN': get_arg, 'GET_FORMULA': get_arg,
    'GET_STRING': get_arg, 'GET_OBJECT': get_arg, 'NUMERIC': var_arg,
    'STRING': var_arg, 'BOOLEAN': var_arg, 'CONDITION_EQUAL': var_arg,
    'CONDITION_NOT_EQUAL': var_arg, 'COUNT': list_arg, 'SORT': sort_arg,
    'OR': list_arg, 'AND': list_arg, 'FILTER_COMPARABLE': filter_arg,
    'FILTER_OBJECT': filter_arg, 'EQUAL': equal_arg, 'MIN': list_arg, 'MAX': list_arg,
    'SERVER_FILTER_NUMERIC': filter_arg, 'SERVER_FILTER_BOOL': filter_arg,
    'SERVER_COUNT': list_arg, 'SERVER_MIN': list_arg,
    'SERVER_MAX': list_arg
};