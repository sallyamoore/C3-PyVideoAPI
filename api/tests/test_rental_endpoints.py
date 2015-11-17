from django.test import TestCase, Client
from api.models import Customer, Movie, Rental
from datetime import datetime, timedelta

# to run tests with coverage: coverage run --source='.' --omit='api/migrations/*,PyVideoAPI/*,api/management/*' manage.py test api
# then to get the coverage report: coverage report -m

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
        response = self.client.get('/rentals/')
        movie = Movie.objects.get(id=1)
        customer = Customer.objects.get(id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.data[0]['movie'], movie.pk)
        self.assertEqual(response.data[0]['customer'], customer.pk)

    def test_invalid_customer_checkout(self):
        """ Does not check out a movie, does not decrement movie num_available or customer account_credit """
        response = self.client.post('/rentals/checkout/', {'movie': 'Jaws', 'customer': '100'})
        movie = Movie.objects.get(id=1)
        customer = Customer.objects.get(id=1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(len(Rental.objects.all()), 1)
        self.assertEqual(movie.num_available, 5)
        self.assertEqual(customer.account_credit, 1799.00)

    def test_invalid_movie_checkout(self):
        """ Does not check out a movie, does not decrement movie num_available or customer account_credit """
        response = self.client.post('/rentals/checkout/', {'movie': 'The Shining', 'customer': '1'})
        customer = Customer.objects.get(id=1)
        movie = Movie.objects.get(id=1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(len(Rental.objects.all()), 1)
        self.assertEqual(movie.title, "Jaws")
        self.assertEqual(movie.num_available, 5)
        self.assertEqual(customer.account_credit, 1799.00)

    def test_valid_checkout(self):
        """ Checks out a movie. Decrements the movie num_available and the customer account_credit """
        response = self.client.post('/rentals/checkout/', {'movie': 'Jaws', 'customer': '1'})
        rental = Rental.objects.last()
        movie = Movie.objects.get(id=1)
        customer = Customer.objects.get(id=1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(len(Rental.objects.all()), 2)
        self.assertEqual(rental.checked_out, True)
        self.assertEqual(movie.num_available, 4)
        self.assertEqual(customer.account_credit, 1798.00)
