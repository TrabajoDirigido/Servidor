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
    pass

  def tearDown(self):
    pass

  def test_parse_query(self):
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
      my_connected_clients={'0.0.0.0':'ble'}
      parsed_query,_ = parse_query(parsed_query,1,my_connected_clients)
      #print(parsed_query)
      save_parsed_query_to_database(parsed_query,my_connected_clients)
      #print(Query.objects.get(id=1).query)
      client_side_query = get_client_side_query(parsed_query,my_connected_clients)

      #print(client_side_query)
      for r in Query.objects.get(id=2).results.all():
          print(r.value)
      self.assertEquals(1,1)


