#__author__ = 'Camila Alvarez'
from django.test import TestCase
from ServerClient.utils import parse_query
from ServerClient.client_side_utils import get_client_side_query
from ServerClient.database_utils import save_parsed_query_to_database
from django.test.utils import setup_test_environment
from ServerClient.models import Argument,Query, Result, Lab


class ParseQueryTest(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.my_connected_clients={'0.0.0.0':'ble'}
        try:
            self.lab = Lab.objects.get(lab='test').id
        except Exception as e:
            self.lab = Lab(lab='test',seccion='1')
            self.lab.save()
            self.lab= self.lab.id

    def tearDown(self):
        pass

    def test_logic(self):
        parsed_query = {'method': 'logic',
                        'type': 'and',
                        'vals': {'method': 'compare',
                                'arg1': [{'type':'bool', 'var':True}, {'method': 'compare',
                                                'arg1': [{'type':'int', 'var':2}],
                                                'arg2': [{'type':'int', 'var':3}]}],
                                'arg2': [{'method': 'compare',
                                                'arg1': [{'type':'int', 'var':2}],
                                                'arg2': [{'type':'int', 'var':2}]}, {'type':'bool', 'var':False}]}
                    }
        parsed_query,_ = parse_query(parsed_query,1,self.my_connected_clients)
        #print(parsed_query)
        save_parsed_query_to_database(parsed_query,self.my_connected_clients,self.lab)

        client_side_query = get_client_side_query(parsed_query,self.my_connected_clients)
        res = [eval(r.value) for r in Result.objects.filter(query=Query.objects.get(id=1))]
        self.assertEquals(res,[True])

    def test_filter(self):
        parsed_query = {'method': 'filter',
                        'vals':{'method': 'compare',
                                'arg1': [{'type':'int', 'var':2},{'type':'int', 'var':5},{'type':'int', 'var':6}],
                                'arg2': [{'type':'int', 'var':3},{'type':'int', 'var':4},{'type':'int', 'var':6}]},
                        'type': 'equal',
                        'var': {'type':'bool', 'var':True}
                        }
        parsed_query,_ = parse_query(parsed_query,1,self.my_connected_clients)
        print(parsed_query)
        save_parsed_query_to_database(parsed_query,self.my_connected_clients,self.lab)

        client_side_query = get_client_side_query(parsed_query,self.my_connected_clients)
        res = [eval(r.value) for r in Result.objects.filter(query=Query.objects.get(id=1))]
        self.assertEquals(res,[True])


    def test_filter_2(self):
        parsed_query = {'method': 'filter',
                        'vals':{'method': 'compare',
                                'arg1': [{'type':'int', 'var':2},{'type':'int', 'var':5},{'type':'int', 'var':6}],
                                'arg2': [{'type':'int', 'var':3},{'type':'int', 'var':4},{'type':'int', 'var':6}]},
                        'type': 'equal',
                        'var': {'type':'bool', 'var':False}
                        }
        parsed_query,_ = parse_query(parsed_query,1,self.my_connected_clients)
        print(parsed_query)
        save_parsed_query_to_database(parsed_query,self.my_connected_clients,self.lab)

        client_side_query = get_client_side_query(parsed_query,self.my_connected_clients)
        res = [eval(r.value) for r in Result.objects.filter(query=Query.objects.get(id=1))]
        self.assertEquals(res,[False, False])


    def test_filter_3(self):
        parsed_query = {'method': 'filter',
                        'vals':{'method': 'compare',
                                'arg1': [{'type':'int', 'var':2},{'type':'int', 'var':5},{'type':'int', 'var':6}],
                                'arg2': [{'type':'int', 'var':3},{'type':'int', 'var':4},{'type':'int', 'var':6}]},
                        'type': 'equal',
                        'var': {'type':'int', 'var':3}
                        }
        parsed_query,_ = parse_query(parsed_query,1,self.my_connected_clients)
        print(parsed_query)
        save_parsed_query_to_database(parsed_query,self.my_connected_clients,self.lab)

        client_side_query = get_client_side_query(parsed_query,self.my_connected_clients)
        res = [eval(r.value) for r in Result.objects.filter(query=Query.objects.get(id=1))]
        self.assertEquals(res,[])

    def test_count(self):
        parsed_query = {'method': 'count',
                        'vals':{'method': 'compare',
                                'arg1': [{'type':'int', 'var':2},{'type':'int', 'var':5},{'type':'int', 'var':6}],
                                'arg2': [{'type':'int', 'var':3},{'type':'int', 'var':4},{'type':'int', 'var':6}]}
                         }
        parsed_query,_ = parse_query(parsed_query,1,self.my_connected_clients)
        #print(parsed_query)
        save_parsed_query_to_database(parsed_query,self.my_connected_clients,self.lab)

        client_side_query = get_client_side_query(parsed_query,self.my_connected_clients)
        res = [eval(r.value) for r in Result.objects.filter(query=Query.objects.get(id=1))]
        self.assertEquals(res,[3])

    def test_compare_one_value_arg1(self):
        parsed_query = {'method': 'compare',
                        'arg1':[{'type':'int', 'var':1}],
                        'arg2':[{'type':'int', 'var':1},{'type':'int', 'var':2},{'type':'int', 'var':1}]}

        parsed_query,_ = parse_query(parsed_query,1,self.my_connected_clients)
        #print(parsed_query)
        save_parsed_query_to_database(parsed_query,self.my_connected_clients,self.lab)

        client_side_query = get_client_side_query(parsed_query,self.my_connected_clients)
        res = [eval(r.value) for r in Result.objects.filter(query=Query.objects.get(id=1))]
        self.assertEquals(res,[True, False,True])


    def test_compare_one_value_arg2(self):
        parsed_query = {'method': 'compare',
                        'arg2':[{'type':'int', 'var':1}],
                        'arg1':[{'type':'int', 'var':1},{'type':'int', 'var':2},{'type':'int', 'var':1}]}

        parsed_query,_ = parse_query(parsed_query,1,self.my_connected_clients)
        #print(parsed_query)
        save_parsed_query_to_database(parsed_query,self.my_connected_clients,self.lab)

        client_side_query = get_client_side_query(parsed_query,self.my_connected_clients)
        res = [eval(r.value) for r in Result.objects.filter(query=Query.objects.get(id=1))]
        self.assertEquals(res,[True, False,True])

    def test_sort_desc(self):
        parsed_query = {'method': 'sort',
                        'vals':[{'type':'int', 'var':1},{'type':'int', 'var':-1},{'type':'int', 'var':5},
                                {'type':'int', 'var':100},{'type':'int', 'var':46}],
                        'des': {'type': 'bool', 'var':True}
                        }
        parsed_query,_ = parse_query(parsed_query,1,self.my_connected_clients)
        #print(parsed_query)
        save_parsed_query_to_database(parsed_query,self.my_connected_clients,self.lab)

        client_side_query = get_client_side_query(parsed_query,self.my_connected_clients)
        res = [eval(r.value) for r in Result.objects.filter(query=Query.objects.get(id=1))]
        self.assertEquals(res,[100,46,5,1,-1])

    def test_sort_asc(self):
        parsed_query = {'method': 'sort',
                        'vals':[{'type':'int', 'var':1},{'type':'int', 'var':-1},{'type':'int', 'var':5},
                                {'type':'int', 'var':100},{'type':'int', 'var':46}],
                        'des': {'type': 'bool', 'var':False}
                        }
        parsed_query,_ = parse_query(parsed_query,1,self.my_connected_clients)
        #print(parsed_query)
        save_parsed_query_to_database(parsed_query,self.my_connected_clients,self.lab)

        client_side_query = get_client_side_query(parsed_query,self.my_connected_clients)
        res = [eval(r.value) for r in Result.objects.filter(query=Query.objects.get(id=1))]
        self.assertEquals(res,[-1,1,5,46,100])


    def test_min(self):
        parsed_query = {'method': 'min',
                        'vals':[{'type':'int', 'var':1},{'type':'int', 'var':-1},{'type':'int', 'var':5},
                                {'type':'int', 'var':100},{'type':'int', 'var':46}]
                        }
        parsed_query,_ = parse_query(parsed_query,1,self.my_connected_clients)
        #print(parsed_query)
        save_parsed_query_to_database(parsed_query,self.my_connected_clients,self.lab)

        client_side_query = get_client_side_query(parsed_query,self.my_connected_clients)
        res = [eval(r.value) for r in Result.objects.filter(query=Query.objects.get(id=1))]
        self.assertEquals(res,[-1])

    def test_max(self):
        parsed_query = {'method': 'max',
                        'vals':[{'type':'int', 'var':1},{'type':'int', 'var':-1},{'type':'int', 'var':5},
                                {'type':'int', 'var':100},{'type':'int', 'var':46}]
                        }
        parsed_query,_ = parse_query(parsed_query,1,self.my_connected_clients)
        #print(parsed_query)
        save_parsed_query_to_database(parsed_query,self.my_connected_clients,self.lab)

        client_side_query = get_client_side_query(parsed_query,self.my_connected_clients)
        res = [eval(r.value) for r in Result.objects.filter(query=Query.objects.get(id=1))]
        self.assertEquals(res,[100])