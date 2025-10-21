from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

# Authentication
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required

# Custom
from .models import Customer, Car
from .forms import CustomerForm, CarForm, LoginForm
from .utils.utils import UtilsClass

def home(request):
    return render(request, 'home/home.html')

# ------------------------- LOGIN -------------------------

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
        customers = Customer.objects.filter(name__istartswith=p_search)
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
            UtilsClass().save_object_customer(form)
            messages.success(request, 'Customer registered successfully.')
            return redirect('list-customer')
        return render(request, 'customer/form.html', {'form': form, 'edition': False})
    else:
        form = CustomerForm()
        return render(request, 'customer/form.html', {'form': form, 'edition': False})

@login_required(login_url="/login/")
def edit_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            UtilsClass().save_object_customer(form, instance=customer)
            messages.success(request, 'Customer edited successfully.')
            return redirect('show-customer', id=id)
    else:
        form = CustomerForm(initial=UtilsClass().get_data_from_customer(customer))
    return render(request, 'customer/form.html', {'form': form, 'customer': customer, 'edition': True})

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
def create_car(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            UtilsClass().save_object_car(form, customer)
            messages.success(request, 'Car registered successfully.')
            return redirect('show-customer', customer_id)
        return render(request, 'car/form.html', {'form': form, 'edition': False, 'customer': customer})
    else:
        form = CarForm()
    return render(request, 'car/form.html', {'form': form, 'edition': False, 'customer': customer})

def show_car(request, customer_id, car_id):
    customer = get_object_or_404(Customer, id=customer_id)
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'car/show.html', {'customer': customer, 'car': car})

@login_required(login_url="/login/")
def edit_car(request, customer_id, car_id):
    car = get_object_or_404(Car, id=car_id)
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            UtilsClass().save_object_car(form, customer, car=car)
            messages.success(request, 'Car edited successfully.')
            return redirect('show-car', customer_id, car_id)
    else:
        initial_data = UtilsClass().get_data_from_car(car)
        form = CarForm(initial=initial_data, instance=car)

    return render(request, 'car/form.html', {
        'form': form,
        'edition': True,
        'customer': customer,
        'car': car
    })



@login_required(login_url="/login/")
def delete_car(request, customer_id, car_id):
    car = get_object_or_404(Car, id=car_id)
    car.delete()
    messages.success(request, 'Car deleted successfully.')
    return redirect('show-customer', customer_id)

# ------------------------- LOGOUT -------------------------

@login_required(login_url="/login/")
def logout_view(request):
    auth_logout(request)
    messages.success(request, 'Logoff done successfully.')
    return redirect('home')
