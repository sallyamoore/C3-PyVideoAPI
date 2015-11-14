from django.core.management.base import BaseCommand, CommandError
from api.models import Customer, Movie, Rental
import json
from dateutil import parser

class Command(BaseCommand):
    """Loads JSON file and seeds the database."""
    args = "No arguments needed."

    def handle(self, *args, **options):
        Customer.objects.all().delete()
        Movie.objects.all().delete()
        Rental.objects.all().delete()

        with open("api/fixtures/customers.json") as f:
            reader = json.load(f)
            for item in reader:
                _, created = Customer.objects.get_or_create(
                    name=item["name"],
                    registered_at=parser.parse(item["registered_at"]),
                    address=item["address"],
                    city=item["city"],
                    state=item["state"],
                    postal_code=item["postal_code"],
                    phone=item["phone"],
                    account_credit=item["account_credit"]
                )

        with open("api/fixtures/movies.json") as f:
            reader = json.load(f)
            for item in reader:
                _, created = Movie.objects.get_or_create(
                    title=item["title"],
                    overview=item["overview"],
                    release_date=parser.parse(item["release_date"]),
                    inventory=item["inventory"],
                    num_available=item["inventory"],
                )
