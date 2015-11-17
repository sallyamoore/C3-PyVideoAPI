from rest_framework import serializers
from api.models import Customer, Movie, Rental

class ApiCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('pk', 'name', 'registered_at', 'address', 'city', 'state',
            'postal_code', 'phone', 'account_credit')

class ApiMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('pk', 'title', 'overview', 'release_date', 'inventory',
            'num_available')

class ApiRentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ('pk', 'checkout_date', 'return_date', 'movie',
            'customer', 'checked_out')

    # def create(self, validated_data):
    #     movie_data = validated_data.pop('movie')
    #     movie = Movie.objects.get(title=movie_data)
    #     customer_data = validated_data.pop('customer')
    #     customer = Customer.objects.get(pk=customer_data)
    #
    #     print "MOVIE: " + movie_data
    #     print "CUST: " + customer_data
    #
    #     rental = Rental.objects.create(movie=movie_data, customer=customer_data)
    #
    #     rental.save()
    #     return rental
