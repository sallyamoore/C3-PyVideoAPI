from django.test import TestCase, Client
from api.models import Customer, Movie, Rental
from datetime import datetime, timedelta
from decimal import Decimal
from django.core.validators import MinValueValidator, ValidationError

# to run tests with coverage: coverage run --source='.' --omit='api/migrations/*,PyVideoAPI/*,api/management/*' manage.py test api
# then to get the coverage report: coverage report -m

class CustomerTestCase(TestCase):
    def setUp(self):
        Customer.objects.create(
            name="Jean Luc Picard",
            registered_at=datetime.now(),
            address="123 Space", city="Space", state="MW",
            postal_code="its f-ing space dude", phone="555-5555",
            account_credit=56.34
        )

    def test_valid_customer(self):
        """ Adds a customer to the database when valid params given """
        customer = Customer.objects.get(id=1)
        self.assertEqual(customer.name, "Jean Luc Picard")
        self.assertEqual(customer.address, "123 Space")
        self.assertEqual(customer.account_credit, Decimal('56.34'))

    def test_customer_name_is_required(self):
        """ Requires name length to be greater than zero """
        customer = Customer.objects.get(id=1)
        customer.name = ''
        self.assertRaises(ValidationError, customer.save)
        db_customer = Customer.objects.get(id=1)
        self.assertEqual(db_customer.name, 'Jean Luc Picard')

    def test_customer_address_is_required(self):
        """ Requires address length to be greater than zero """
        customer = Customer.objects.get(id=1)
        customer.address = ''
        self.assertRaises(ValidationError, customer.save)
        db_customer = Customer.objects.get(id=1)
        self.assertEqual(db_customer.address, '123 Space')

    def test_customer_city_is_required(self):
        """ Requires city length to be greater than zero """
        customer = Customer.objects.get(id=1)
        customer.city = ''
        self.assertRaises(ValidationError, customer.save)
        db_customer = Customer.objects.get(id=1)
        self.assertEqual(db_customer.city, 'Space')

    def test_customer_state_is_required(self):
        """ Requires state length to be greater than zero """
        customer = Customer.objects.get(id=1)
        customer.state = ''
        self.assertRaises(ValidationError, customer.save)
        db_customer = Customer.objects.get(id=1)
        self.assertEqual(db_customer.state, 'MW')

    def test_customer_postal_code_is_required(self):
        """ Requires postal_code length to be greater than three """
        customer = Customer.objects.get(id=1)
        customer.postal_code = '123'
        self.assertRaises(ValidationError, customer.save)
        db_customer = Customer.objects.get(id=1)
        self.assertEqual(db_customer.postal_code, 'its f-ing space dude')

    def test_customer_phone_is_required(self):
        """ Requires phone length to be greater than six """
        customer = Customer.objects.get(id=1)
        customer.phone = '123456'
        self.assertRaises(ValidationError, customer.save)
        db_customer = Customer.objects.get(id=1)
        self.assertEqual(db_customer.phone, '555-5555')

class MovieTestCase(TestCase):
    def setUp(self):
        Movie.objects.create(
            title="Jaws",
            overview="Sharks are super hungry",
            release_date=datetime.now(),
            inventory=6,
            num_available=6
        )

    def test_valid_movie(self):
        """ Adds a movie to the database when valid params given """
        movie = Movie.objects.get(id=1)
        self.assertEqual("Jaws", movie.title)
        self.assertEqual(movie.inventory, 6)
        self.assertEqual(movie.num_available, 6)

    def test_num_available_less_than_inventory(self):
        """ Does not allow a movie's num_available to exceed inventory. """
        movie = Movie.objects.get(id=1)
        movie.num_available = 9
        self.assertRaises(ValidationError, movie.save)
        db_movie = Movie.objects.get(id=1)
        self.assertEqual(db_movie.num_available, 6)

    def test_num_available_zero_or_greater(self):
        """ A movie's num_available cannot be negative """
        movie = Movie.objects.get(id=1)
        movie.num_available = -2
        self.assertRaises(ValidationError, movie.full_clean)
        db_movie = Movie.objects.get(id=1)
        self.assertEqual(db_movie.num_available, 6)

    def test_inventory_zero_or_greater(self):
        """ A movie's inventory cannot be negative """
        movie = Movie.objects.get(id=1)
        movie.inventory = -2
        self.assertRaises(ValidationError, movie.full_clean)
        db_movie = Movie.objects.get(id=1)
        self.assertEqual(db_movie.inventory, 6)

    def test_movie_rental(self):
        """ A movie can have an associated rental. """
        movie = Movie.objects.get(id=1)
        customer = Customer.objects.create(
            name="Jean Luc Picard",
            registered_at=datetime.now(),
            address="123 Space", city="Space", state="MW",
            postal_code="its f-ing space dude", phone="555-5555",
            account_credit=56.34
        )
        rental = Rental.objects.create(
            checkout_date=datetime.now(),
            return_date=datetime.now() + timedelta(7,0),
            checked_out=True,
            movie=movie,
            customer=customer
        )
        self.assertEqual(len(movie.rental_set.all()), 1)
        self.assertEqual(movie.rental_set.first().pk, 1)

class RentalTestCase(TestCase):
    def setUp(self):
        movie = Movie.objects.create(
            title="Jaws",
            overview="Sharks are super hungry",
            release_date=datetime.now(),
            inventory=6,
            num_available=6
        )
        customer = Customer.objects.create(
            name="Jean Luc Picard",
            registered_at=datetime.now(),
            address="123 Space", city="Space", state="MW",
            postal_code="its f-ing space dude", phone="555-5555",
            account_credit=56.34
        )
        rental = Rental.objects.create(
            checkout_date=datetime.now(),
            return_date=datetime.now() + timedelta(7,0),
            checked_out=True,
            movie=movie,
            customer=customer
        )
    def test_valid_rental(self):
        """ Adds a rental to the database when valid params given """
        rental = Rental.objects.get(id=1)
        self.assertEqual(rental.checked_out, True)
        self.assertEqual(rental.movie.title, 'Jaws')
        self.assertEqual(rental.customer.name, "Jean Luc Picard")

    def test_rental_decrements_movie_num_available(self):
        """ When a rental is saved it decrements the num_available of a movie """
        movie = Movie.objects.get(id=1)
        self.assertEqual(movie.num_available, 5)

    def test_rental_fails_when_no_movies_available(self):
        """ Raises a ValidationError if there are no more movies available to rent """
        movie = Movie.objects.get(id=1)
        movie.num_available = 0
        movie.save()
        customer = Customer.objects.create(
            name="Jean Luc Picard",
            registered_at=datetime.now(),
            address="123 Space", city="Space", state="MW",
            postal_code="its f-ing space dude", phone="555-5555",
            account_credit=56.34
        )
        new_rental = Rental(
            checkout_date=datetime.now(),
            return_date=datetime.now() + timedelta(7,0),
            checked_out=True,
            movie=movie,
            customer=customer
        )
        db_movie = Movie.objects.get(id=1)
        self.assertEqual(db_movie.num_available, 0)
        self.assertRaises(ValidationError, new_rental.save)

class GetAllCustomers(TestCase):
    def setUp(self):
        Customer.objects.create(
            name="Jean Luc Picard",
            registered_at=datetime.now(),
            address="123 Space", city="Space", state="MW",
            postal_code="its f-ing space dude", phone="555-5555",
            account_credit=56.34
        )
        Customer.objects.create(
            name="Trash Panda",
            registered_at=datetime.now(),
            address="123 Your Trash Can", city="Backyard", state="WA",
            postal_code="its a trashcan dude", phone="ima racoon",
            account_credit=1800.00
        )
        self.client = Client()

    def test_get_all_customers(self):
        """ Returns a list of all customers in JSON """
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.data[0]['name'], "Jean Luc Picard")
        self.assertEqual(response.data[1]['name'], "Trash Panda")

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

class GetAllRentals(TestCase):
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
