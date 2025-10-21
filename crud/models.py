from datetime import date, datetime
from decimal import Decimal
from PIL import Image
from django.core.validators import (
    EmailValidator,
    MinValueValidator,
    MaxValueValidator,
    RegexValidator
)
from django.db import models
from django.db.models import Q
from django.db.models.constraints import CheckConstraint, UniqueConstraint

from django.core.exceptions import ValidationError
from .utils.validators import *

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

class Customer(models.Model):
    GENDER = (
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('O', 'OTHER'),
    )

    def default_birthday():
        today = date.today()
        try:
            return date(today.year - 18, today.month, today.day)
        except ValueError:
            return date(today.year - 18, today.month, today.day - 1)

    name = models.CharField(
        "Name",
        max_length=75,
        null=False,
        blank=False,
        error_messages={
            'blank': 'Name is empty.',
            'null': 'Name is required.',
            'max_length': 'Name cannot exceed 75 characters.'
        }
    )

    email = models.EmailField(
        "E-mail",
        max_length=50,
        null=False,
        blank=False,
        validators = [
            validate_email,
            EmailValidator(message="Invalid e-mail.")
        ],
        error_messages={
            'blank': 'E-mail is empty.',
            'null': 'E-mail is required.',
            'invalid': 'Invalid e-mail',
            'max_length': 'E-mail cannot exceed 50 characters.'
        }
    )
   
    salary = models.DecimalField(
        "Salary",
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        null=False,
        blank=False,
        validators = [
            validate_salary,
            MinValueValidator(Decimal(0.00), message="Salary must be greater than or equal to 0.00."),
            MaxValueValidator(Decimal(999999999.99), message="Salary cannot exceed 999,999,999.99."),
        ],
        error_messages={
            'blank': 'Salary is empty.',
            'null': 'Salary is required.',
            'invalid': 'Invalid salary.'
        }
    )

    birthday = models.DateField(
        "Birthday",
        default=default_birthday,
        null=False,
        blank=False,
        validators=[validate_birthday],
        error_messages={
            'blank': 'Birthday cannot be empty.',
            'null': 'Birthday is required.',
            'invalid': 'Enter a valid date (YYYY-MM-DD).'
        }
    )

    gender = models.CharField(
        "Gender",
        max_length=1,
        choices=GENDER,
        default='M',
        null=False,
        blank=False,
        validators=[validate_gender],
        error_messages={
            'blank': 'Gender is empty.',
            'null': 'Gender is required.',
            'invalid_choice': 'Invalid gender.'
        }
    )

    picture = models.ImageField(
        "Picture",
        upload_to='customers',
        blank=False,
        null=False,
        default='customers/noimage.jpg',
        error_messages={
            'blank': 'Picture is empty.',
            'null': 'Picture is null.',
            'invalid': 'Invalid picture file.'
        }
    )

    def __str__(self):
        return f"{self.pk}: {self.name}"

    class Meta:
        db_table = 'customer'
        ordering=['-id']
        managed = True
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        constraints = [
            UniqueConstraint(fields=['email'], 
                             name='unq_customer_email', 
                             violation_error_message="E-mail already registered."),
            CheckConstraint(check=Q(salary__gte=0.00) & Q(salary__lte=999999999.99), 
                            name='chk_customer_salary', 
                            violation_error_message="Invalid salary."),
            CheckConstraint(check=Q(gender__in=['M','F','O']), 
                            name='chk_customer_gender', 
                            violation_error_message="Invalid gender."),
        ]
        
    
# ---------------------------------------------------------------------------------------------------------------------------------------------------------


class Car(models.Model):

    def get_current_year():
        return date.today().year
    
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        verbose_name="Customer",
        error_messages={
            'null': 'Customer is required.',
            'blank': 'Please select a valid customer.',
        }
    )

    model = models.CharField(
        "Model",
        max_length=45,
        default="",
        blank=False,
        null=False,
        error_messages={
            'blank': 'Model is empty.',
            'null': 'Model is required.',
            'max_length': 'Model name cannot exceed 45 characters.',
        }
    )

    plate = models.CharField(
        "License Plate",
        max_length=9,
        blank=False,
        null=False,
        validators=[
            validate_plate,
            RegexValidator(
                regex=r'^[A-Z]{3}\d[A-Z]\d{2}$|^[A-Z]{3}-\d{4}$',
                message='Enter a valid plate (e.g., ABC-1234 or ABC1D23).',
                code='invalid_plate'
            )
        ],
        error_messages={
            'blank': 'Plate is empty.',
            'null': 'Plate is required.',
            'max_length': 'Platee must have a maximum of 7 characters.',
        }
    )
    
    year = models.PositiveIntegerField(
        "Year",
        blank=False,
        null=False,
        validators=[
            validate_year,
            MinValueValidator(1885, message="Year must be greater than 1885 (first automobile)."),
            max_year_validator,
        ],
        error_messages={
            'blank': 'Year is empty.',
            'null': 'Year is required',
            'invalid': 'Invalid year.',
        }
    )

    market_value = models.DecimalField(
        "Market Value",
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        blank=False,
        null=False,
        validators = [
            validate_market_value,
            MinValueValidator(Decimal(0.00), message="Market value must be greater than or equal to 0.00."),
            MaxValueValidator(Decimal(999999999.99), message="Market value cannot exceed 999,999,999.99."),
        ],
        error_messages={
            'blank': 'Market value is empty.',
            'null': 'Market value is required.',
            'invalid': 'Invalid market value.',
        }
    )

    picture = models.ImageField(
        "Picture",
        upload_to='cars',
        default='cars/noimage.jpg',
        blank=False,
        null=False,
        error_messages={
            'invalid_image': 'Invalid picture file.',
            'blank': 'Picture is empty.',
            'null': 'Picture is required.',
        }
    )

    description = models.CharField(
        "Description",
        max_length=200,
        default="",
        blank=True,
        null=True,
        error_messages={
            'max_length': 'Description cannot exceed 200 characters.',
        }
    )

    def __str__(self):
        return f"{self.pk}: {self.model} - {self.year} - {self.market_value}"

    class Meta:
        db_table = 'car'
        ordering=['-id']
        managed = True
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'
        constraints = [
            UniqueConstraint(fields=['plate'], name="unq_car_plate", violation_error_message="Plate already registered."),
            CheckConstraint(check=Q(market_value__gte=Decimal(0.00)) & Q(market_value__lte=Decimal(999999999.99)), name="check_car_market_value", violation_error_message="Invalid salary."),
        ]

   