from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Customer, Movie, Rental
from api.serializers import ApiCustomerSerializer, ApiMovieSerializer, ApiRentalSerializer

@api_view(['GET'])
def customer_list(request):
    """
    List all customers.
    """
    if request.method == 'GET':
        customers = Customer.objects.all()
        serializer = ApiCustomerSerializer(customers, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def movie_list(request):
    """
    List all movies.
    """
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = ApiMovieSerializer(movies, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def rental_list(request):
    """
    List all rentals.
    """
    if request.method == 'GET':
        rentals = Rental.objects.all()
        serializer = ApiRentalSerializer(rentals, many=True)
        return Response(serializer.data)
