from django.test import TestCase
from api.models import Customer, Movie, Rental
from datetime import datetime
from decimal import Decimal
from django.core.validators import MinValueValidator, ValidationError

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
        self.assertEqual("Jean Luc Picard", customer.name)
        self.assertEqual("123 Space", customer.address)
        self.assertEqual(Decimal('56.34'), customer.account_credit)

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
        self.assertEqual(6, movie.inventory)
        self.assertEqual(6, movie.num_available)

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
