import time

from django.test import TestCase, Client

from stations.models import Station, StationLog


class NewStationListTest(TestCase):
    @classmethod
    def setUpClass(cls):
        client = Client()
    
    @classmethod
    def tearDownClass(cls):
        Station.objects.all().delete()
        StationLog.objects.all().delete()

    def test_get_all_success(self):
        response = self.client.get('/stations/update', content_type = 'application/json')

        self.assertEqual(response.json(),{'message':"SUCCESS"})
        self.assertEqual(response.status_code, 200)

    def test_get_log_success(self):
        response = self.client.get('/stations/update', content_type = 'application/json')
        first_id = Station.objects.first().id
        last_id = Station.objects.last().id
        time.sleep(10)
        response = self.client.get('/stations/update', content_type = 'application/json')
        
        self.assertEqual(response.json(),{'message':"SUCCESS"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Station.objects.get(id=first_id), Station.objects.get(id=first_id))
        self.assertEqual(Station.objects.get(id=last_id), Station.objects.get(id=last_id))
        self.assertEqual(StationLog.objects.filter(station_id=first_id).count(), 2)
        self.assertEqual(StationLog.objects.filter(station_id=last_id).count(), 2)