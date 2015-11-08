__author__ = 'Camila Alvarez'
from ServerClient.utils import parse_query,get_client_side_query
from ServerClient.database_utils import save_parsed_query_to_database
parsed_query = {'method': 'compare',
                'arg1':[2],
                'arg2':[3]
                }

id = 1
dict={'0.0.0.0':'ble'}
parsed_query, _ = parse_query(parsed_query,id, dict)
save_parsed_query_to_database(parsed_query,dict)
print(parsed_query)

print(get_client_side_query(parsed_query,dict))