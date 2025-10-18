from django.urls import re_path, include
from django.contrib import admin
from django.conf.urls.static import static
from djangoproject import settings
from crud import views

admin.autodiscover()

urlpatterns = [
    re_path(r'^', include('crud.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^login/$', views.login_view, name='login-view'),
    re_path(r'^logout/$', views.logout_view, name='logout-view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)