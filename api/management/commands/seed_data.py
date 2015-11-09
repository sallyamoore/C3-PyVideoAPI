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

        with open("api/fixtures/rentals.json") as f:
            reader = json.load(f)
            for item in reader:
                checked = True if item["checked_out"] == "true" else False
                _, created = Rental.objects.get_or_create(
                    checkout_date=parser.parse(item["checkout_date"]),
                    return_date=parser.parse(item["return_date"]),
                    movie_id=item["movie_id"],
                    customer_id=item["customer_id"],
                    checked_out=checked
                )

        for rental in Rental.objects.all():
            if rental.checked_out == True:
                movie = Movie.objects.get(id=rental.movie_id)
                movie.num_available -= 1


        # Rental.objects.all(
        #     num_available=Case(
        #         When()
        #     ),
        # )
        # # WIP
        # # movies = Movie.objects.all()
        # # select all rentals where movie_id = this and checked_out = true
        # # for movie in movies:
        #
        # # for each movie, subtract num checked out from num_available
        # # select * from movie where movie.rentals eq true
        #
        # Rentals
        # when Rental checked_out == true
        #     that movie_id, find movie and subtract one from num_available
