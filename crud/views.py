from datetime import datetime
from decimal import Decimal

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

# Authentication
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Customer, Car
from .forms import CustomerForm, CarForm, LoginForm

# -----

def save_object_customer(form, instance=None):
    if instance:
        customer = instance
    else:
        customer = Customer()

    customer.name = form.cleaned_data['name']
    customer.email = form.cleaned_data['email']
    customer.birthday = form.cleaned_data['birthday']
    customer.gender = form.cleaned_data['gender']
    customer.salary = form.cleaned_data['salary']

    if form.cleaned_data.get('picture'):
        customer.picture = form.cleaned_data['picture']

    customer.save()

def save_object_car(form, customer, car=None):
    data = form.cleaned_data

    if car is None:
        # Criar novo
        car = Car.objects.create(
            model=data['model'],
            year=data['year'],
            market_value=data['market_value'],
            plate=data['plate'],
            description=data['description'],
            picture=data['picture'],
            customer=customer
        )
    else:
        # Atualizar existente
        car.model = data['model']
        car.year = data['year']
        car.market_value = data['market_value']
        car.plate = data['plate']
        car.description = data['description']

        picture = data.get('picture')
        if picture:
            car.picture = picture  # atualiza só se tiver foto nova

        car.customer = customer
        car.save()

    return car

def get_data_from_customer(customer):
    initial_data = {
        'name': customer.name,
        'email': customer.email,
        'salary': str(customer.salary).replace(",","."),
        'birthday': customer.birthday.strftime("%d/%m/%Y"),
        'gender': customer.gender,
        'picture': customer.picture,
    }
    return initial_data

def get_data_from_car(car):
    initial_data = {
        'id': car.pk or None,
        'model': car.model,
        'plate': car.plate,
        'market_value': str(car.market_value).replace(",","."),
        'year': car.year,
        'description': car.description,
        'picture': car.picture,
    }
    return initial_data
   
# -----

def home(request):
    return render(request, 'home/home.html')

def show_car(request, idcust, idcar):
    customer = get_object_or_404(Customer, id=idcust)
    car = get_object_or_404(Car, id=idcar)
    return render(request, 'car/show.html', {'customer': customer, 'car': car})

def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "User already logged in.")
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'User logged in successfully.')
                return redirect('home')
            else:
                form.add_error(None, "Username and password don't match.")
    else:
        form = LoginForm()

    return render(request, 'login/login.html', {'form': form})

def catalog(request):
    cars = Car.objects.all()
    paginator = Paginator(cars, 7)
    page = request.GET.get('page')
    try:
        cars = paginator.page(page)
    except PageNotAnInteger:
        cars = paginator.page(1)
    except EmptyPage:
        cars = paginator.page(paginator.num_pages)
    return render(request, 'car/catalog.html', {'cars': cars})

# ------------------------- CUSTOMER -------------------------

@login_required(login_url="/login/")
def list_customer(request):
    if request.method == 'POST':
        p_search = request.POST['search'] + '%'
        customers = Customer.objects.extra(where=["name LIKE %s"], params=[p_search])
    else:
        customers = Customer.objects.all()

    paginator = Paginator(customers, 10)
    page = request.GET.get('page')
    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)

    return render(request, 'customer/list.html', {'customers': customers})

@login_required(login_url="/login/")
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            save_object_customer(form)
            messages.success(request, 'Customer registered successfully.')
            return redirect('list-customer')
        return render(request, 'customer/create.html', {'form': form})
    else:
        form = CustomerForm()
    return render(request, 'customer/create.html', {'form': form})

@login_required(login_url="/login/")
def edit_customer(request, id):
    customer = get_object_or_404(Customer, id=id)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            save_object_customer(form, instance=customer)
            messages.success(request, 'Customer edited successfully.')
            return redirect('show-customer', id=id)
    else:
        form = CustomerForm(initial=get_data_from_customer(customer), instance=customer)

    return render(request, 'customer/edit.html', {'form': form, 'customer': customer})

@login_required(login_url="/login/")
def delete_customer_confirmation(request, id):
    customer = get_object_or_404(Customer, id=id)
    return render(request, 'customer/confirmation.html', {'customer': customer})

@login_required(login_url="/login/")
def delete_customer(request, id):
    if Car.objects.filter(customer=id).exists():
        messages.error(request, 'Client has registered cars and cannot be deleted.')
    else:
        customer = get_object_or_404(Customer, id=id)
        customer.delete()
        messages.success(request, 'Customer deleted successfully.')
    return redirect('list-customer')

@login_required(login_url="/login/")
def show_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    customer.gender = 'Male' if customer.gender == 'M' else 'Female'

    cars = Car.objects.filter(customer=id)
    paginator = Paginator(cars, 5)
    page = request.GET.get('page')
    try:
        cars = paginator.page(page)
    except PageNotAnInteger:
        cars = paginator.page(1)
    except EmptyPage:
        cars = paginator.page(paginator.num_pages)

    return render(request, 'customer/show.html', {'customer': customer, 'cars': cars})

# ------------------------- CAR -------------------------

@login_required(login_url="/login/")
def create_car(request, idcust):
    customer = get_object_or_404(Customer, id=idcust)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            save_object_car(form, customer)
            messages.success(request, 'Car registered successfully.')
            return redirect('show-customer', idcust)
        return render(request, 'car/create.html', {'form': form, 'customer': customer})
    else:
        form = CarForm(initial={'model': '', 'market_value': Decimal('0.00'), 'description': ''})
    return render(request, 'car/create.html', {'form': form, 'customer': customer})

@login_required(login_url="/login/")
def edit_car(request, idcust, idcar):
    car = get_object_or_404(Car, id=idcar)
    customer = get_object_or_404(Customer, id=idcust)

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            save_object_car(form, customer, car=car)
            messages.success(request, 'Car edited successfully.')
            return redirect('show-customer', idcust)
    else:
        initial_data = get_data_from_car(car) 
        form = CarForm(initial=initial_data, instance=car)

    return render(request, 'car/edit.html', {
        'form': form,
        'customer': customer,
        'car': car
    })

@login_required(login_url="/login/")
def delete_car_confirmation(request, idcust, idcar):
    car = get_object_or_404(Car, id=idcar)
    customer = get_object_or_404(Customer, id=idcust)
    return render(request, 'car/confirmation.html', {'car': car, 'customer': customer})

@login_required(login_url="/login/")
def delete_car(request, idcust, idcar):
    car = get_object_or_404(Car, id=idcar)
    car.delete()
    messages.success(request, 'Car deleted successfully.')
    return redirect('show-customer', car.customer_id)

# ------------------------- LOGOUT -------------------------

@login_required(login_url="/login/")
def logout_view(request):
    auth_logout(request)
    messages.success(request, 'Logoff done successfully.')
    return redirect('home')


