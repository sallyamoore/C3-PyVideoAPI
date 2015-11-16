from django.test import TestCase, Client
from api.models import Customer, Movie, Rental
from datetime import datetime, timedelta

class RentalEndpoints(TestCase):
    def setUp(self):
        movie = Movie.objects.create(
            title="Jaws",
            overview="Sharks are super hungry",
            release_date=datetime.now(),
            inventory=6,
            num_available=6
        )
        customer = Customer.objects.create(
            name="Trash Panda",
            registered_at=datetime.now(),
            address="123 Your Trash Can", city="Backyard", state="WA",
            postal_code="its a trashcan dude", phone="ima racoon",
            account_credit=1800.00
        )
        Rental.objects.create(
            checkout_date=datetime.now(),
            return_date=datetime.now() + timedelta(7,0),
            checked_out=True,
            movie=movie,
            customer=customer
        )
        self.client = Client()

    def test_get_all_rentals(self):
        """ Returns a list of all rentals in JSON """
        movie = Movie.objects.get(id=1)
        customer = Customer.objects.get(id=1)
        response = self.client.get('/rentals/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.data[0]['movie'], movie.pk)
        self.assertEqual(response.data[0]['customer'], customer.pk)
