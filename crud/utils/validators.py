from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from datetime import date
from decimal import Decimal

def validate_name(value):
    if not value:
        raise ValidationError("Name is empty.")
    if value and len(value) < 5:
        raise ValidationError("Invalid name.")
    return value

def validate_birthday(value):
    if not value:
        raise ValidationError("Birthday is empty.")
    today = date.today()
    min_date = date(today.year - 130, today.month, today.day)
    max_date = date(today.year - 18, today.month, today.day)

    if value < min_date:
        raise ValidationError("Date of birth cannot be more than 130 years ago.")
    if value > max_date:
        raise ValidationError("You must be at least 18 years old.")
    return value

def validate_email(value):
    if not value:
        raise ValidationError("E-mail is empty.")
    validator = EmailValidator(message="Invalid e-mail.")
    validator(value)
    from crud.models import Customer
    count = Customer.objects.filter(email__exact=value).count()
    if count > 0:
        raise ValidationError("E-mail already registered.")
    return value

"""
def validate_decimal_value(label):
    def validate(value):
        if value is None:
            raise ValidationError(f"{label.capitalize()} is empty.")
        if value < Decimal('0.00') or value > Decimal('999999999.99'):
            raise ValidationError(f"Invalid {label.lower()}.")
        return value 
    return validate
"""

def validate_salary(value):
    if value is None:
        raise ValidationError(f"Salary is empty.")
    if value < Decimal('0.00') or value > Decimal('999999999.99'):
        raise ValidationError(f"Invalid salary.")
    return value 

def validate_gender(value):
    if not value:
        raise ValidationError("Gender is empty.")
    if value not in ['M', 'F', 'O']:
        raise ValidationError("Invalid gender.")
    return value

def validate_picture(value):
    if not value:
        raise ValidationError("Picture is empty.")
    return value

def validate_plate(value):
    if not value:
        raise ValidationError("Plate is empty.")
    validator = RegexValidator(
            regex=r'^[A-Z]{3}\d[A-Z]\d{2}$|^[A-Z]{3}-\d{4}$',
            message='Enter a valid plate (e.g., ABC-1234 or ABC1D23).',
            code='invalid_plate'
    )
    validator(value)
    from crud.models import Car
    count = Car.objects.filter(plate__exact=value).count()
    if count > 0:
        raise ValidationError("Plate already registered.")
    return value

def validate_year(value):
    if value is None:
        raise ValidationError("Year is empty.")
    today = date.today()
    if value < 1885 or value > today.year + 1:
        raise ValidationError(f"Year must be between 1885 and {today.year + 1}.")
    return value

def validate_market_value(value):
    if value is None:
        raise ValidationError(f"Market Value is empty.")
    if value < Decimal('0.00') or value > Decimal('999999999.99'):
        raise ValidationError(f"Invalid market value.")
    return value 

def max_year_validator(value):
    max_year = date.today().year + 1
    if value > max_year:
        raise ValidationError(f"Year cannot exceed {max_year}.")
