from django.test import TestCase
from api.models import Customer, Movie, Rental
from datetime import datetime, timedelta
from django.core.validators import ValidationError

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

    def test_rental_movie_id(self):
        rental = Rental.objects.get(id=1)
        movie = Movie.objects.get(id=1)
        self.assertEqual(rental.rental_movie_id(), movie.id)

    def test_rental_customer_id(self):
        rental = Rental.objects.get(id=1)
        customer = Customer.objects.get(id=1)
        self.assertEqual(rental.rental_customer_id(), customer.id)
