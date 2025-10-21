from crud.models import Customer, Car

class UtilsClass():
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(UtilsClass, cls).__new__(cls)
        return cls.__instance

    def save_object_customer(self, form, instance=None):
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

    def save_object_car(self, form, customer, car=None):
        data = form.cleaned_data

        if car is None:
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

    def get_data_from_customer(self, customer):
        initial_data = {
            'name': customer.name,
            'email': customer.email,
            'salary': str(customer.salary).replace(",","."),
            'birthday': customer.birthday.strftime("%d/%m/%Y"),
            'gender': customer.gender,
            'picture': customer.picture,
        }
        return initial_data

    def get_data_from_car(self, car):
        initial_data = {
            'id': car.id or None,
            'model': car.model,
            'plate': car.plate,
            'market_value': str(car.market_value).replace(",","."),
            'year': car.year,
            'description': car.description,
            'picture': car.picture,
        }
        return initial_data