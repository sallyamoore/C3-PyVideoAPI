from django.test import TestCase
from api.models import Customer, Movie, Rental
from datetime import datetime
from decimal import Decimal

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

    def test_customer_required_attributes(self):
        customer = Customer.objects.get(id=1)
        customer.name = 
        self.assertEqual(False, customer.save())
