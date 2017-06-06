from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('crud.views',
    url(r'^crud/', include('crud.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', auth_views.login, {'template_name': 'user/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,{'next_page': '/crud'}, name='logout'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
