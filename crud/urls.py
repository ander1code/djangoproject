from django.conf.urls import patterns, include, url
from crud import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('crud.views',
    url ( r'customer/$' , views.list_customer , name='list_customer' ) ,
    url ( r'customer/new/$' , views.create_customer, name='create_customer' ) ,
    url ( r'customer/(?P<id>\d+)/edit/$' , views.edit_customer , name='edit_customer' ) ,
    url ( r'customer/(?P<id>\d+)/delete/$' , views.delete_customer , name='delete_customer' ) ,
    url ( r'customer/(?P<id>\d+)/show/$' , views.show_customer , name='show_customer' ) ,
    url ( r'customer/(?P<idcust>\d+)/car/new/$' , views.create_car, name='create_car' ) ,
    url ( r'customer/(?P<idcust>\d+)/car/(?P<idcar>\d+)/edit/$' , views.edit_car , name='edit_car' ) ,
    url ( r'customer/(?P<idcust>\d+)/car/(?P<idcar>\d+)/delete/$' , views.delete_car , name='delete_car' ) ,
    url ( r'customer/(?P<idcust>\d+)/car/(?P<idcar>\d+)/show/$' , views.show_car , name='show_car' ) ,
    url ( r'^$' , views.home , name='home' ),
    url ( r'catalog$', views.do_Catalog, name='do_Catalog'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
