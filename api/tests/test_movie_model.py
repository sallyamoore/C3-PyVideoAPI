from django.test import TestCase
from api.models import Customer, Movie, Rental
from datetime import datetime, timedelta
from django.core.validators import ValidationError

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
        movie = Movie.objects.get(pk=1)
        self.assertEqual("Jaws", movie.title)
        self.assertEqual(movie.inventory, 6)
        self.assertEqual(movie.num_available, 6)

    def test_num_available_less_than_inventory(self):
        """ Does not allow a movie's num_available to exceed inventory. """
        movie = Movie.objects.get(pk=1)
        movie.num_available = 9
        self.assertRaises(ValidationError, movie.save)
        db_movie = Movie.objects.get(pk=1)
        self.assertEqual(db_movie.num_available, 6)

    def test_num_available_zero_or_greater(self):
        """ A movie's num_available cannot be negative """
        movie = Movie.objects.get(pk=1)
        movie.num_available = -2
        self.assertRaises(ValidationError, movie.full_clean)
        db_movie = Movie.objects.get(pk=1)
        self.assertEqual(db_movie.num_available, 6)

    def test_inventory_zero_or_greater(self):
        """ A movie's inventory cannot be negative """
        movie = Movie.objects.get(pk=1)
        movie.inventory = -2
        self.assertRaises(ValidationError, movie.full_clean)
        db_movie = Movie.objects.get(pk=1)
        self.assertEqual(db_movie.inventory, 6)

    def test_movie_rental(self):
        """ A movie can have an associated rental. """
        movie = Movie.objects.get(pk=1)
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
