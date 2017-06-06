from django import forms
from .models import  *
import datetime

from django.core.exceptions import ValidationError

class CustomerForm(forms.ModelForm):
    imageCustomer = forms.ImageField ()
    birthday = forms.DateField(initial=date.today().replace(year=date.today().year - 18).strftime("%d/%m/%Y"))

    class Meta:
        model = Customer

    def __init__(self , *args , **kwargs):
        super ( CustomerForm , self ).__init__ ( *args , **kwargs )
        self.fields['name'].error_messages['required'] = 'Name is empty.'
        self.fields['email'].error_messages['required'] = 'Email is empty.'
        self.fields['salary'].error_messages['required'] = 'Salary is empty.'
        self.fields['birthday'].error_messages['required'] = 'Birthday is empty.'
        self.fields['gender'].error_messages['required'] = 'Gender is empty.'
        self.fields['imageCustomer'].error_messages['required'] = 'Image is empty.'
        self.fields['email'].error_messages['invalid'] = 'Invalid Email.'
        self.fields['salary'].error_messages['invalid'] = 'Invalid Salary.'
        self.fields['birthday'].error_messages['invalid'] = 'Invalid Birthday.'
        self.fields['birthday'].widget.attrs['readonly'] = True

    def clean_salary(self):
        salary = self.cleaned_data['salary']
        if salary < 0:
            raise forms.ValidationError("Salary can not be less than zero.")
        return salary

    def clean_birthday(self):
        birthday = self.cleaned_data['birthday']
        if(birthday != ""):
            today_18 = datetime.date ( year=datetime.datetime.now ( ).year - 18 , month=datetime.datetime.now ( ).month ,
                                       day=datetime.datetime.now ( ).day )
            birthday = self.cleaned_data['birthday']
            if not birthday <= today_18:
                raise forms.ValidationError("Customer must be 18 years or older.")
            return birthday
        else:
          raise forms.ValidationError("Birthday is empty.")  

class CustomerCarForm(forms.ModelForm):
    id = forms.IntegerField ( widget=forms.TextInput ( attrs={'readonly': 'readonly'} ) )
    name = forms.CharField ( widget=forms.TextInput ( attrs={'readonly': 'readonly'} ) )
    class Meta:
        model = Customer
        fields = ['id','name']

    def __init__(self , *args , **kwargs):
        super ( CustomerCarForm , self ).__init__ ( *args , **kwargs )
        self.fields['id'].error_messages['required'] = 'ID is empty.'


class CarForm(forms.ModelForm):
    plate = forms.RegexField (initial="",  regex=r'^[A-Z]{3}\d{4}$' , max_length=7 , error_message='Invalid plate. (EX: AAA1111)' )
    yearCar = forms.RegexField (initial="",   regex=r'^\d{4}$' , min_length=4 , max_length=4 , error_message="Invalid car's year" )
    marketVal = forms.DecimalField (initial="",   max_digits=12 , decimal_places=2)

    class Meta:
        model = Car
    
    def __init__(self , *args , **kwargs):
        super ( CarForm , self ).__init__ ( *args , **kwargs )
        self.fields['model'].error_messages['required'] = 'Model is empty.'
        self.fields['plate'].error_messages['required'] = 'Plate is empty.'
        self.fields['yearCar'].error_messages['required'] = "Year's car is empty."
        self.fields['marketVal'].error_messages['required'] = "Market's value is empty."
        self.fields['imageCar'].error_messages['required'] = "Car's image is empty."
        self.fields['description'].error_messages['required'] = "Description is empty."
        