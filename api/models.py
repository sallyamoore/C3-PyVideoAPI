from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, ValidationError

class Customer(models.Model):
    name = models.CharField(max_length=255)
    registered_at = models.DateTimeField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    account_credit = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Customer Model methods go here.

# Validates that num_available is less than inventory in the Movie model
def validate_num_available(num):
    if num > self.inventory:
        raise ValidationError("Number available cannot exceed inventory.")
# Another option is to put this at start of class:
    # def clean(self):
    #     from django.core.exceptions import ValidationError
    #     if self.num_available > self.inventory:
    #         raise ValidationError('Number available cannot exceed inventory.')

class Movie(models.Model):
    title = models.CharField(max_length=255)
    overview = models.TextField()
    release_date = models.DateTimeField()
    inventory = models.PositiveSmallIntegerField()
    num_available = models.PositiveSmallIntegerField(
        validators=[validate_num_available])
    rentals = models.ManyToManyField(Customer, through='Rental', through_fields=('movie', 'customer'))
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Rental(models.Model):
    checkout_date = models.DateTimeField()
    return_date = models.DateTimeField()
    movie = models.ForeignKey('Movie', on_delete=models.DO_NOTHING)
    customer = models.ForeignKey('Customer', on_delete=models.DO_NOTHING)
    checked_out = models.BooleanField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
