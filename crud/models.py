from django.db import models
from decimal import Decimal
from django.core.validators import RegexValidator
from datetime import date

from PIL import Image

class Customer(models.Model):
    name = models.CharField(max_length=100, default="")
    email = models.EmailField(unique = True, default="")
    salary = models.DecimalField(max_digits=12,decimal_places=2,default=Decimal('0.00'))
    birthday = models.DateField(default=date.today().replace(year=date.today().year - 18).strftime("%d/%m/%Y"), blank=True)
    GENDER = (('M','MALE'),('F','FEMALE'))
    gender = models.CharField(max_length=1, choices=GENDER, default='M')
    imageCustomer = models.ImageField ( upload_to='media', blank=True, null=True, default='no_image.png' )

    def __unicode__(self):
        return "%s -- %s" % (self.id, self.name)

class Car(models.Model):
    customer = models.ForeignKey ( Customer , on_delete=models.CASCADE )
    model = models.CharField ( max_length=100, default="")
    plate = models.CharField ( max_length=7, unique=True, default="")
    yearCar = models.IntegerField (default="")
    marketVal = models.DecimalField(max_digits=12,decimal_places=2,default=Decimal('0.00'))
    imageCar = models.ImageField ( upload_to='media' , blank=True , null=True , default='no_image.png' )
    description = models.CharField(max_length=200, default="")

    def __unicode__(self):
        return "%s -- %s -- %d" % (self.id, self.model, self.yearCar)