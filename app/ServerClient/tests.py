#__author__ = 'Camila Alvarez'
from django.test import TestCase
from ServerClient.utils import parse_query, get_client_side_query
from ServerClient.database_utils import save_parsed_query_to_database
from django.test.utils import setup_test_environment
from ServerClient.models import Argument,Query

class ParseQueryTest(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.my_connected_clients={'0.0.0.0':'ble'}

    def tearDown(self):
        pass

    def test_logic(self):
        parsed_query = {'method': 'logic',
                        'type': 'and',
                        'vals': {'method': 'compare',
                                'arg1': [True, {'method': 'compare',
                                                'arg1': [2],
                                                'arg2': [3]}],
                                'arg2': [{'method': 'compare',
                                                'arg1': [2],
                                                'arg2': [2]}, False]}
                    }
        parsed_query,_ = parse_query(parsed_query,1,self.my_connected_clients)
        print(parsed_query)
        save_parsed_query_to_database(parsed_query,self.my_connected_clients)

        client_side_query = get_client_side_query(parsed_query,self.my_connected_clients)
        res = [eval(r.value) for r in Query.objects.get(id=1).results.all()]
        self.assertEquals(res,[True])

    def test_count(self):
        parsed_query = {'method': 'count',
                        'vals':{'method': 'compare',
                                'arg1': [2,5,6],
                                'arg2': [3,4,6]}
                         }
        parsed_query,_ = parse_query(parsed_query,1,self.my_connected_clients)
        print(parsed_query)
        save_parsed_query_to_database(parsed_query,self.my_connected_clients)

        client_side_query = get_client_side_query(parsed_query,self.my_connected_clients)
        res = [eval(r.value) for r in Query.objects.get(id=1).results.all()]
        self.assertEquals(res,[3])

    def test_sort_desc(self):
        parsed_query = {'method': 'sort',
                        'vals':[1,-1,5,100,46],
                        'desc': True
                        }
        parsed_query,_ = parse_query(parsed_query,1,self.my_connected_clients)
        print(parsed_query)
        save_parsed_query_to_database(parsed_query,self.my_connected_clients)

        client_side_query = get_client_side_query(parsed_query,self.my_connected_clients)
        res = [eval(r.value) for r in Query.objects.get(id=1).results.all()]
        self.assertEquals(res,[100,46,5,1,-1])

    def test_sort_asc(self):
        parsed_query = {'method': 'sort',
                        'vals':[1,-1,5,100,46],
                        'desc': False
                        }
        parsed_query,_ = parse_query(parsed_query,1,self.my_connected_clients)
        print(parsed_query)
        save_parsed_query_to_database(parsed_query,self.my_connected_clients)

        client_side_query = get_client_side_query(parsed_query,self.my_connected_clients)
        res = [eval(r.value) for r in Query.objects.get(id=1).results.all()]
        self.assertEquals(res,[-1,1,5,46,100])


    def test_min(self):
        parsed_query = {'method': 'min',
                        'vals':[1,-1,5,100,46]
                        }
        parsed_query,_ = parse_query(parsed_query,1,self.my_connected_clients)
        print(parsed_query)
        save_parsed_query_to_database(parsed_query,self.my_connected_clients)

        client_side_query = get_client_side_query(parsed_query,self.my_connected_clients)
        res = [eval(r.value) for r in Query.objects.get(id=1).results.all()]
        self.assertEquals(res,[-1])

    def test_max(self):
        parsed_query = {'method': 'max',
                        'vals':[1,-1,5,100,46]
                        }
        parsed_query,_ = parse_query(parsed_query,1,self.my_connected_clients)
        print(parsed_query)
        save_parsed_query_to_database(parsed_query,self.my_connected_clients)

        client_side_query = get_client_side_query(parsed_query,self.my_connected_clients)
        res = [eval(r.value) for r in Query.objects.get(id=1).results.all()]
        self.assertEquals(res,[100])