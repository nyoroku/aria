from . import views
from django.conf.urls import url


app_name = 'home'
urlpatterns = [
         url(r'^$', views.index, name='index'),
         url(r'^allnews/', views.allnews, name='allnews'),
         url(r'^new/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' \
           r'(?P<new>[-\w]+)/$',
           views.latest_detail,
           name='news'),


         ]


