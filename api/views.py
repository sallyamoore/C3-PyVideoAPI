from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Customer, Movie, Rental
from api.serializers import ApiCustomerSerializer, ApiMovieSerializer, ApiRentalSerializer

from django.core.paginator import Paginator

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
def customers_by_name(request):
    """
    Retrieve a subset of customers sorted by name.
    """
    if request.method == 'GET':
        customers = Customer.objects.all().order_by('name')
        limit = request.query_params.get('limit')
        offset = request.query_params.get('offset')
        paginator = Paginator(customers, limit)
        customers = paginator.page(offset)
        serializer = ApiCustomerSerializer(customers, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def customers_by_registered_at(request):
    """
    Retrieve a subset of customers sorted by registered_at.
    """
    if request.method == 'GET':
        customers = Customer.objects.all().order_by('registered_at')
        limit = request.query_params.get('limit')
        offset = request.query_params.get('offset')
        paginator = Paginator(customers, limit)
        customers = paginator.page(offset)
        serializer = ApiCustomerSerializer(customers, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def customers_by_postal_code(request):
    """
    Retrieve a subset of customers sorted by postal_code.
    """
    if request.method == 'GET':
        customers = Customer.objects.all().order_by('postal_code')
        limit = request.query_params.get('limit')
        offset = request.query_params.get('offset')
        paginator = Paginator(customers, limit)
        customers = paginator.page(offset)
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
