from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from djangoproject import settings
from django.contrib.auth import login, logout, views as auth_views
from crud import views

admin.autodiscover()

urlpatterns = [
	url(r'^crud/', include('crud.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, {'template_name':'user/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/crud'}, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

