from rest_framework import serializers
from api.models import Customer, Movie, Rental

class ApiCustomerSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    registered_at = serializers.DateTimeField()
    address = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=255)
    state = serializers.CharField(max_length=255)
    postal_code = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=255)
    account_credit = serializers.DecimalField(
        max_digits=7,
        decimal_places=2
    )
