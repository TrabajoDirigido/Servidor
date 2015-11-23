/**
 * Created by Camila Alvarez on 20-11-2015.
 */
var options = ['GET', 'COUNT', 'OR', 'AND'];

var get_array = ['GET_COMPARABLE', 'GET_OBJECT'];
var get_comparable_array = ['GET_DOUBLE', 'GET_BOOLEAN', 'GET_FORMULA', 'GET_STRING'];

var count_array = ['FILTER'];
var or_and_array = ['AND', 'OR', 'EQUAL'];

var equal_array = ['GET', 'VAR', 'SORT','EQUAL','FILTER'];
var sort_array = ['GET_COMPARABLE', 'FILTER_COMPARABLE', 'EQUAL'];

var filter_array = ['FILTER_OBJECT', 'FILTER_COMPARABLE'];
var filter_object_array = ['GET_OBJECT'];
var filter_comparable_array = ['GET_COMPARABLE', 'EQUAL', 'SORT'];

var vars = ['DOUBLE', 'STRING', 'BOOLEAN'];

var query_dict = {
    'GET': [get_array], 'GET_COMPARABLE': [get_comparable_array],
    'COUNT': [count_array], 'OR': [or_and_array], 'AND': [or_and_array], 'EQUAL': [equal_array,equal_array],
    'SORT': [sort_array], 'FILTER': [filter_array], 'FILTER_OBJECT': [filter_object_array],
    'FILTER_COMPARABLE': [filter_comparable_array], 'VAR': [vars], 'COMPARE':[equal_array]
};

var get_arg = ['OBJETIVO:', 'Y: ', 'X: ' ];
var var_arg = ['VALOR: '];
var list_arg = ['ARGUMENTOS:   ['];
var equal_arg = ['ARG1:   [', 'ARG2:   ['];


var argument_dict = {
    'GET_DOUBLE': get_arg, 'GET_BOOLEAN': get_arg, 'GET_FORMULA': get_arg,
    'GET_STRING': get_arg, 'GET_OBJECT': get_arg, 'DOUBLE': var_arg,
    'STRING': var_arg, 'BOOLEAN': var_arg, 'CONDITION_EQUAL': var_arg,
    'CONDITION_NOT_EQUAL': var_arg, 'COUNT': list_arg, 'SORT': list_arg,
    'OR': list_arg, 'AND': list_arg, 'FILTER_COMPARABLE': list_arg,
    'FILTER_OBJECT': list_arg, 'EQUAL': equal_arg
};