from django.test import TestCase, Client
from api.models import Movie
from datetime import datetime, timedelta

class MovieEndpoints(TestCase):
    def setUp(self):
        Movie.objects.create(
            title="Jaws",
            overview="Sharks are super hungry",
            release_date=datetime.now(),
            inventory=6,
            num_available=6
        )
        Movie.objects.create(
            title="The Shining",
            overview="Family vacation gone wrong",
            release_date=datetime.now(),
            inventory=8,
            num_available=8
        )
        self.client = Client()

    def test_get_all_movies(self):
        """ Returns a list of all movies in JSON """
        response = self.client.get('/movies/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.data[0]['title'], "Jaws")
        self.assertEqual(response.data[1]['title'], "The Shining")

    def test_get_movie_by_title(self):
        """ GET /movie/(?P<title>.+) retrieves a single movie by title """
        response = self.client.get('/movie/Jaws/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.data['title'], 'Jaws')
        self.assertEqual(response.data['inventory'], 6)

    def test_get_movies_sorted_by_column(self):
        """ Given sort column of overview, limit of 2, and page of 1, returns
        matching movie, i.e., Aliens """
        Movie.objects.create(
            title="Aliens",
            overview="AAAALLLIENS!!!",
            release_date=datetime.now() - timedelta(1,0),
            inventory=1,
            num_available=1
        )
        columns = [ 'title', 'overview', 'release_date', 'inventory',
        'num_available' ]

        for col in columns:
            response = self.client.get('/movies/' + col + '/?limit=2&page=1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data), 2)
            self.assertEqual(response['Content-Type'], 'application/json')
            self.assertEqual(response.data[0]['title'], "Aliens")
