from django.http import HttpResponseRedirect
from django.shortcuts import redirect , render , get_object_or_404 , get_list_or_404
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from . import *
from django.contrib import messages

# Authentication
from django.contrib.auth import login , logout , authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.urls import reverse


def home(request):
    print('Home')
    return render ( request , 'home.html' )


def show_car(request , idcust , idcar):
    customer = get_object_or_404 ( Customer , id=idcust )
    car = get_object_or_404 ( Car , id=idcar )
    return render ( request , 'car/show.html' , {'customer': customer , 'car': car} )


def do_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
             messages.info ( request , "User already logged in." )
             return render ( request , 'home.html')
        else:
            return render ( request , 'user/login.html')

    if request.method == 'POST':
        user = authenticate ( username=request.POST.get ( 'username' ) , password=request.POST.get ( 'password' ) )
        if user is not None:
            login ( request , user )
            messages.success ( request , 'User logged in successfully.' )
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.error ( request , "User and password don't match." )
            return render ( request , 'home.html')


def do_Catalog(request):
    print('Home')
    cars = Car.objects.all ( )
    paginator = Paginator ( cars , 7 )
    page = request.GET.get ( 'page' )
    try:
        cars = paginator.page ( page )
    except PageNotAnInteger:
        cars = paginator.page ( 1 )
    except EmptyPage:
        cars = paginator.page ( paginator.num_pages )
    return render ( request , 'car/catalog.html' , {'cars': cars} )


@login_required ( login_url="/login/" )
def list_customer(request):
    if request.method == 'POST':
        p_search = request.POST['search'] + '%'
        customers = Customer.objects.extra ( where=["name LIKE %s"] , params=[p_search] )
        paginator = Paginator ( customers , 10 )
        page = request.GET.get ( 'page' )
        try:
            customers = paginator.page ( page )
        except PageNotAnInteger:
            customers = paginator.page ( 1 )
        except EmptyPage:
            customers = paginator.page ( paginator.num_pages )
        return render ( request , 'customer/list.html' , {'customers': customers} )

    else:
        customers = Customer.objects.all ( )
        paginator = Paginator ( customers , 10 )
        page = request.GET.get ( 'page' )
        try:
            customers = paginator.page ( page )
        except PageNotAnInteger:
            customers = paginator.page ( 1 )
        except EmptyPage:
            customers = paginator.page ( paginator.num_pages )
        return render ( request , 'customer/list.html' , {'customers': customers} )


@login_required ( login_url="/login/" )
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm ( request.POST , request.FILES )
        if form.is_valid ( ):
            customer = form.save ( commit=False )
            customer.name = form.cleaned_data.get ( 'name' )
            customer.email = form.cleaned_data.get ( 'email' )
            customer.salary = form.cleaned_data.get ( 'salary' )
            birthday = datetime.datetime.strptime ( str ( form.cleaned_data.get ( 'birthday' ) ) , '%Y-%m-%d' )
            customer.birthday = birthday
            customer.gender = form.cleaned_data.get ( 'gender' )
            customer.imageCustomer = form.cleaned_data.get ( 'imageCustomer' )
            customer.save ( )
            messages.success ( request , 'Customer registered successfully.' )
            # return HttpResponseRedirect ( 'crud.views.list_customer' )
            return HttpResponseRedirect(reverse('list_customer'))
        else:
            return render ( request , 'customer/create.html' , {'form': form} )
    else:
        form = CustomerForm ( )
        return render ( request , 'customer/create.html' , {'form': form} )


@login_required ( login_url="/login/" )
def edit_customer(request , id):
    customer = get_object_or_404 ( Customer , id=id )
    if request.method == 'POST':
        form = CustomerForm ( request.POST , request.FILES , instance=customer )
        if form.is_valid ( ):
            customer = form.save ( commit=False )
            customer.name = form.cleaned_data.get ( 'name' )
            customer.email = form.cleaned_data.get ( 'email' )
            customer.salary = form.cleaned_data.get ( 'salary' )
            birthday = datetime.datetime.strptime ( str ( form.cleaned_data.get ( 'birthday' ) ) , '%Y-%m-%d' )
            customer.birthday = birthday
            customer.gender = form.cleaned_data.get ( 'gender' )
            customer.imageCustomer = form.cleaned_data.get ( 'imageCustomer' )
            customer.save ( )
            if customer.gender == 'M':
                customer.gender = 'Male'
            else:
                customer.gender = 'Female'

            messages.success ( request , 'Customer edited successfully.' )
            return HttpResponseRedirect(reverse('show_customer', args=(id,)))
    else:
        form = CustomerForm ( initial={'id': customer.id ,
                                       'name': customer.name ,
                                       'email': customer.email ,
                                       'salary': customer.salary ,
                                       'birthday': datetime.datetime.strptime ( str ( customer.birthday ) ,
                                                                                '%Y-%m-%d' ).strftime ( '%d/%m/%Y' ) ,
                                       'gender': customer.gender ,
                                       'imageCustomer': customer.imageCustomer} )
    return render ( request , 'customer/edit.html' , {'form': form, 'customer':customer} )


@login_required ( login_url="/login/" )
def delete_customer_confirmation(request , id):
    customer = get_object_or_404 ( Customer , id=id )
    return render ( request , 'customer/confirmation.html' , {'customer': customer} )


@login_required ( login_url="/login/" )
def delete_customer(request , id):
    if Car.objects.filter ( customer=id ).count ( ) == 0:
        customer = get_object_or_404 ( Customer , id=id )
        customer.delete ( )
        messages.success ( request , 'Customer deleted successfully.' )
    else:
        messages.error ( request , 'Client has registered cars and can not be excluded.' )
    return HttpResponseRedirect(reverse('list_customer'))


@login_required ( login_url="/login/" )
def show_customer(request , id):
    customer = get_object_or_404 ( Customer , id=id )
    if customer.gender == 'M':
        customer.gender = 'Male'
    else:
        customer.gender = 'Female'

    cars = Car.objects.filter ( customer=id )
    paginator = Paginator ( cars , 5 )
    page = request.GET.get ( 'page' )
    try:
        cars = paginator.page ( page )
    except PageNotAnInteger:
        cars = paginator.page ( 1 )
    except EmptyPage:
        cars = paginator.page ( paginator.num_pages )
    return render ( request , 'customer/show.html' , {'customer': customer , 'cars': cars} )


@login_required ( login_url="/login/" )
def create_car(request , idcust):
    if request.method == 'POST':
        form = CarForm ( request.POST , request.FILES )
        if form.is_valid ( ):
            car = form.save ( commit=False )
            car.customer_id = idcust
            car.model = form.cleaned_data.get ( 'model' )
            car.plate = form.cleaned_data.get ( 'plate' )
            car.yearCar = form.cleaned_data.get ( 'yearCar' )
            car.marketVal = form.cleaned_data.get ( 'marketVal' )
            car.description = form.cleaned_data.get ( 'description' )
            car.imageCar = form.cleaned_data.get ( 'imageCar' )
            car.save ( )
            messages.success ( request , 'Car registered successfully.' )
            return HttpResponseRedirect(reverse('show_customer', args=(idcust,)))
        else:
            customer = get_object_or_404 ( Customer , id=idcust )
            return render ( request , 'car/create.html' , {'form': form , 'customer': customer} )
    else:
        customer = get_object_or_404 ( Customer , id=idcust )
        form = CarForm (initial={'model': '', 'marketVal': '0.00', 'description':'' })
    return render ( request , 'car/create.html' , {'form': form , 'customer': customer} )


@login_required ( login_url="/login/" )
def edit_car(request , idcust , idcar):
    car = get_object_or_404 ( Car , id=idcar )
    if request.method == 'POST':
        form = CarForm ( request.POST , request.FILES , instance=car )
        if form.is_valid ( ):
            car = form.save ( commit=False )
            car.customer_id = idcust
            car.model = form.cleaned_data.get ( 'model' )
            car.plate = form.cleaned_data.get ( 'plate' )
            car.yearCar = form.cleaned_data.get ( 'yearCar' )
            car.marketVal = form.cleaned_data.get ( 'marketVal' )
            car.description = form.cleaned_data.get ( 'description' )
            car.imageCar = form.cleaned_data.get ( 'imageCar' )
            car.save ( )
            messages.success ( request , 'Car edited successfully.' )
            return HttpResponseRedirect(reverse('show_customer', args=(idcust,)))
        else:
            customer = get_object_or_404 ( Customer , id=idcust )
            return render ( request , 'car/create.html' , {'form': form , 'customer': customer} )
    else:
        customer = get_object_or_404 ( Customer , id=idcust )
        form = CarForm ( initial={
            'model': car.model ,
            'plate': car.plate ,
            'yearCar': car.yearCar ,
            'marketVal': car.marketVal ,
            'description': car.description ,
            'imageCar': car.imageCar ,
        } )
    return render ( request , 'car/edit.html' , {'form': form , 'customer': customer, 'car':car} )


@login_required ( login_url="/login/" )
def delete_car_confirmation(request , idcust , idcar):
    car = get_object_or_404 ( Car , id=idcar )
    customer = get_object_or_404 ( Customer , id=idcust )
    return render ( request , 'car/confirmation.html' , {'car': car , 'customer': customer} )


@login_required ( login_url="/login/" )
def delete_car(request , idcust , idcar):
    car = get_object_or_404 ( Car , id=idcar )
    car.delete ( )
    messages.success ( request , 'Car deleted successfully.' )
    return HttpResponseRedirect(reverse('show_customer', args=(car.customer_id,)))


@login_required ( login_url="/login/" )
def do_logout(request):
    logout ( request )
    messages.success ( request , 'Logoff done successfully.' )
    return render ( request , 'user/login.html' )
