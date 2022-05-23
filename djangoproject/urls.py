from django.urls import re_path, include
from django.contrib import admin
from django.conf.urls.static import static
from djangoproject import settings
from crud import views

admin.autodiscover()

urlpatterns = [
    re_path(r'^', include('crud.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^login/$', views.do_login, name='do_login'),
    re_path(r'^logout/$', views.do_logout, name='do_logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



