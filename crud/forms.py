from django import forms
from .models import  *
import datetime
from django.core.exceptions import ValidationError

class CustomerForm(forms.ModelForm):
    def __init__(self , *args , **kwargs):
        super ( CustomerForm , self ).__init__ ( *args , **kwargs )
        name = forms.CharField(error_messages={'required': 'Name is empty.'})
        email = forms.EmailField(error_messages={'required': 'Email is empty.'})
        salary = forms.DecimalField(error_messages={'required': 'Salary is empty.', 'invalid': 'Invalid Salary.'})
        gender = forms.ChoiceField(error_messages={'required': 'Gender is empty.'})
        imageCustomer = forms.FileField(error_messages={'required': 'Image is empty.'})
        email = forms.EmailField(error_messages={'invalid': 'Invalid Email.'})
        birthday = forms.DateField(initial=date.today().replace(year=date.today().year - 18).strftime("%d/%m/%Y"), error_messages={'required': 'Birthday is empty.', 'invalid': 'Invalid Birthday.'})
        birthday.widget.attrs['readonly'] = True

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

    class Meta:
        model = Customer
        fields = "__all__"

class CustomerCarForm(forms.ModelForm):

    def __init__(self , *args , **kwargs):
        super ( CustomerCarForm , self ).__init__ ( *args , **kwargs )
        id = forms.CharField(error_messages={'required': 'ID is empty.'})	
        id = forms.IntegerField ( widget=forms.TextInput ( attrs={'readonly': 'readonly'} ) )
        name = forms.CharField ( widget=forms.TextInput ( attrs={'readonly': 'readonly'} ) )

    class Meta:
        model = Customer
        fields = "__all__" 

class CarForm(forms.ModelForm):
    model = forms.CharField(error_messages={'required': 'Model is empty.'})
    plate = forms.RegexField (initial="",  regex=r'^[A-Z]{3}\d{4}$' , max_length=7, error_messages={'invalid': 'Invalid plate. (EX: AAA1111)', 'required': 'Plate is empty.'})
    yearCar = forms.RegexField (initial="",   regex=r'^\d{4}$' , min_length=4 , max_length=4, error_messages={'invalid': "Invalid car's year.", 'required': 'Year is empty.'} )
    marketVal = forms.DecimalField(initial="",   max_digits=12 , decimal_places=2, error_messages={'required': 'Market Value is empty.', 'invalid':'Invalid Market value.'})
    imageCar = forms.ImageField(error_messages={'required': 'Car image is empty.'})
    description = forms.CharField(error_messages={'required': 'Description is empty.'})

    class Meta:
        model = Car
        fields = "__all__"