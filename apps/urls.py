from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from home.views import index


from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns





urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^home/', include('home.urls')),
    url(r'^clothes/', include('clothes.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),
    url(r'^chaining/', include('smart_selects.urls')),
    #url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),







]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


