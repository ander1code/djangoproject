from django.urls import re_path
from django.conf.urls.static import static
from djangoproject import settings
from . import views

urlpatterns = [
    re_path ( r'^$' , views.home, name="home"),
    re_path ( r'catalog$', views.catalog, name="catalog"),
    re_path ( r'customer/$' , views.list_customer, name="list-customer") ,
    re_path ( r'customer/new/$' , views.create_customer, name="create-customer") ,
    re_path ( r'customer/(?P<id>\d+)/edit/$' , views.edit_customer, name="edit-customer") ,
    re_path ( r'customer/(?P<id>\d+)/delete/$' , views.delete_customer, name="delete-customer") ,
    re_path ( r'customer/(?P<id>\d+)/show/$' , views.show_customer, name="show-customer") ,
    re_path ( r'customer/(?P<idcust>\d+)/car/new/$' , views.create_car, name="create-car") ,
    re_path ( r'customer/(?P<idcust>\d+)/car/(?P<idcar>\d+)/edit/$' , views.edit_car, name="edit-car") ,
    re_path ( r'customer/(?P<idcust>\d+)/car/(?P<idcar>\d+)/delete/$' , views.delete_car, name="delete-car") ,
    re_path ( r'customer/(?P<idcust>\d+)/car/(?P<idcar>\d+)/show/$' , views.show_car, name="show-car") ,
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)