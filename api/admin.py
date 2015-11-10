from django.contrib import admin
from .models import Customer, Movie, Rental

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'registered_at', 'address', 'city', 'state',
        'postal_code', 'phone', 'account_credit')

class MovieAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'release_date', 'inventory', 'num_available')

class RentalAdmin(admin.ModelAdmin):
    list_display = ('pk', 'checkout_date', 'return_date', 'rental_movie_id', 'rental_customer_id', 'checked_out')

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Rental, RentalAdmin)
