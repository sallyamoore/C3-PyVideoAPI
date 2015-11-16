from django.test import TestCase, Client
from api.models import Customer
from datetime import datetime, timedelta

class CustomerEndpoints(TestCase):
    def setUp(self):
        Customer.objects.create(
            name="Trash Panda",
            registered_at=datetime.now(),
            address="123 Your Trash Can", city="Backyard", state="WA",
            postal_code="its a trashcan dude", phone="ima racoon",
            account_credit=1800.00
        )
        Customer.objects.create(
            name="Jean Luc Picard",
            registered_at=datetime.now(),
            address="123 Space", city="Space", state="MW",
            postal_code="its f-ing space dude", phone="555-5555",
            account_credit=56.34
        )
        self.client = Client()

    def test_get_all_customers(self):
        """ Returns a list of all customers in JSON """
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.data[0]['name'], "Trash Panda")
        self.assertEqual(response.data[1]['name'], "Jean Luc Picard")

    def test_get_customers_sorted_by_column(self):
        """ Given sort column of name, limit of 2, and page of 1, returns
        matching customer, i.e., Aaron Aaronson """
        Customer.objects.create(
            name="Aaron Aaronson",
            registered_at=datetime.now() - timedelta(1,0),
            address="100 A St", city="Atlanta", state="AZ",
            postal_code="00001", phone="111-1111",
            account_credit=1.00
        )
        columns = [ 'name', 'registered_at', 'address', 'city', 'state',
        'postal_code', 'account_credit' ]

        for col in columns:
            response = self.client.get('/customers/' + col + '/?limit=2&page=1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data), 2)
            self.assertEqual(response['Content-Type'], 'application/json')
            self.assertEqual(response.data[0]['name'], "Aaron Aaronson")
