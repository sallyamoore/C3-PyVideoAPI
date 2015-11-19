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
def customers_by_column(request, column):
    """
    Retrieve a subset of customers sorted by name.
    """
    if request.method == 'GET':
        customers = Customer.objects.all().order_by(column)
        limit = request.query_params.get('limit')
        page = request.query_params.get('page')
        paginator = Paginator(customers, limit)
        customers = paginator.page(page)
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
def movies_by_column(request, column):
    """
    Retrieve a subset of movies sorted by column.
    """
    if request.method == 'GET':
        movies = Movie.objects.all().order_by(column)
        limit = request.query_params.get('limit')
        page = request.query_params.get('page')
        paginator = Paginator(movies, limit)
        movies = paginator.page(page)
        serializer = ApiMovieSerializer(movies, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def movie(request, title):
    """
    Retrieve a movie by entering its title.
    """
    if request.method == 'GET':
        movies = Movie.objects.get(title=title)
        serializer = ApiMovieSerializer(movies)
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

@api_view(['POST', 'PUT'])
def checkout_checkin(request, **kwargs):
    """ Check out and check in rentals """
    if request.method == 'POST':
        if Movie.objects.filter(title=request.data["movie"]).exists() and Customer.objects.filter(pk=request.data["customer"]).exists():
            movie = Movie.objects.get(title=request.data["movie"])
            customer = Customer.objects.get(pk=request.data["customer"])

            rental_dict = { 'movie': movie.pk, 'customer': customer.pk }

            rental = Rental( movie=movie, customer=customer )
            rental.checkout()

            serializer = ApiRentalSerializer(data=rental_dict)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        if Movie.objects.filter(title=kwargs["movie_title"]).exists() and Customer.objects.filter(pk=kwargs["customer_pk"]).exists():
            movie = Movie.objects.get(title=kwargs["movie_title"])
            customer_pk = kwargs["customer_pk"]

            # checks in the oldest rental if multiple copies of the same movie are checked out by the same customer
            rental = Rental.objects.filter(movie=movie.pk, customer=customer_pk).first()
            rental_dict = rental.checkin()

            serializer = ApiRentalSerializer(data=rental_dict)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)
