from django.urls import re_path
from django.conf.urls.static import static
from djangoproject import settings
from . import views

urlpatterns = [
    re_path ( r'^$' , views.home, name="home"),
    re_path ( r'catalog$', views.do_Catalog, name="do_Catalog"),
    re_path ( r'customer/$' , views.list_customer, name="list_customer") ,
    re_path ( r'customer/new/$' , views.create_customer, name="create_customer") ,
    re_path ( r'customer/(?P<id>\d+)/edit/$' , views.edit_customer, name="edit_customer") ,
    re_path ( r'customer/(?P<id>\d+)/delete/$' , views.delete_customer, name="delete_customer") ,
    re_path ( r'customer/(?P<id>\d+)/show/$' , views.show_customer, name="show_customer") ,
    re_path ( r'customer/(?P<idcust>\d+)/car/new/$' , views.create_car, name="create_car") ,
    re_path ( r'customer/(?P<idcust>\d+)/car/(?P<idcar>\d+)/edit/$' , views.edit_car, name="edit_car") ,
    re_path ( r'customer/(?P<idcust>\d+)/car/(?P<idcar>\d+)/delete/$' , views.delete_car, name="delete_car") ,
    re_path ( r'customer/(?P<idcust>\d+)/car/(?P<idcar>\d+)/show/$' , views.show_car, name="show_car") ,
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)