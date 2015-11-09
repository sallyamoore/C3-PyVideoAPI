from django.contrib import admin
from .models import Customer, Movie, Rental

admin.site.register(Customer)
admin.site.register(Movie)
admin.site.register(Rental)
