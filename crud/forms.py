from datetime import date
from decimal import Decimal
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Customer, Car
from .utils.validators import (
    validate_name,
    validate_birthday,
    validate_email,
    validate_salary,
    validate_gender,
    validate_picture,
    validate_plate,
    validate_year,
    validate_market_value
)

# --------------------------------------------------------------------------------------------

from django import forms

class LoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

    username = forms.CharField(
        max_length=20,
        error_messages={'required': 'Username is empty.'},
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        max_length=20,
        error_messages={'required': 'Password is empty.'},
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

    def clean_username(self):
        data = self.cleaned_data["username"]
        if not data:
            raise ValidationError("Username is empty.")
        return data
    
    def clean_password(self):
        data = self.cleaned_data["password"]
        if not data:
            raise ValidationError("Password is empty.")
        return data

   
# --------------------------------------------------------------------------------------------

class CustomerForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = False

        for name, field in self.fields.items():
            if self.initial.get(name) is None:
                self.initial[name] = ''

        if self.initial.get('picture'):
            self.fields['picture'].required = False

    name = forms.CharField(
        max_length=75,
        required=True,
        error_messages={'required': 'Name is empty.'}
    )

    email = forms.EmailField(
        max_length=50,
        required=True,
        error_messages={
            'required': 'E-mail is empty.',
            'invalid': 'Invalid e-mail.',
        }
    )

    salary = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=True,
        validators=[
            MinValueValidator(Decimal('0.00'), message="Salary must be greater than or equal to 0.00."),
            MaxValueValidator(Decimal('999999999.99'), message="Salary cannot exceed 999,999,999.99.")
        ],
        error_messages={
            'required': 'Salary is empty.',
            'invalid': 'Invalid salary.'
        }
    )

    birthday = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=date.today().replace(year=date.today().year - 18),
        error_messages={
            'required': 'Birthday is empty.',
            'invalid': 'Invalid birthday.',
        }
    )

    gender = forms.ChoiceField(
        choices=Customer.GENDER,
        required=True,
        error_messages={'required': 'Gender is empty.'}
    )

    picture = forms.ImageField(
        required=True,
        error_messages={
            'required': 'Picture is empty.',
            'invalid': 'Invalid picture file.'
        }
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        validate_name(name) 
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if self.instance and getattr(self.instance, 'id', None):
            original_email = self.instance.email
            if email == original_email:
                return email

            if Customer.objects.filter(email=email).exclude(id=self.instance.id).exists():
                raise ValidationError("E-mail already registered.")
        else:
            if Customer.objects.filter(email=email).exists():
                raise ValidationError("E-mail already registered.")

        if not email:
            raise ValidationError("E-mail is empty.")

        validate_email(email)
        return email

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        validate_birthday(birthday)
        return birthday

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        validate_salary(salary)
        return salary

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        validate_gender(gender)
        return gender
    
    def clean_picture(self):
        picture = self.cleaned_data.get('picture')

        if not picture and not self.fields['picture'].required:
            return self.initial.get('picture')

        validate_picture(picture)
        return picture


# --------------------------------------------------------------------------------------------

class CarForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = False

        for name, field in self.fields.items():
            if self.initial.get(name) is None:
                self.initial[name] = ''

        if self.initial.get('picture'):
            self.fields['picture'].required = False

    model = forms.CharField(
        error_messages={'required': 'Model is empty.'}
    )

    plate = forms.CharField(
        max_length=9,
        error_messages={
            'invalid': 'Invalid plate. (EX: ABC-1234 or ABC1D23)',
            'required': 'Plate is empty.'
        }
    )

    year = forms.IntegerField(
        error_messages={
            'invalid': "Invalid car's year.",
            'required': 'Year is empty.'
        }
    )

    market_value = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        error_messages={
            'required': 'Market Value is empty.',
            'invalid': 'Invalid Market value.'
        }
    )

    picture = forms.ImageField(
        error_messages={'required': 'Picture is empty.'}
    )

    description = forms.CharField(
        error_messages={'required': 'Description is empty.'}
    )

    def clean_plate(self):
        plate = self.cleaned_data.get('plate')

        if self.instance and plate == self.instance.plate:
            return plate

        if not plate:
            raise ValidationError("Plate is empty.")

        exclude_id = self.instance.id if self.instance else None

        qs = Car.objects.filter(plate=plate)
        if exclude_id is not None:
            qs = qs.exclude(id=exclude_id)

        if qs.exists():
            raise ValidationError("Plate already registered.")

        validate_plate(plate)
        return plate

    def clean_year(self):
        value = self.cleaned_data.get('year')
        return validate_year(value)

    def clean_market_value(self):
        value = self.cleaned_data.get('market_value')
        return validate_market_value(value)

    def clean_model(self):
        value = self.cleaned_data.get('model')
        if not value:
            raise ValidationError("Model is empty.")
        return value

    def clean_description(self):
        value = self.cleaned_data.get('description')
        if not value:
            raise ValidationError("Description is empty.")
        return value

    def clean_picture(self):
        picture = self.cleaned_data.get('picture')

        if not picture and not self.fields['picture'].required:
            return self.initial.get('picture')

        validate_picture(picture)
        return picture

