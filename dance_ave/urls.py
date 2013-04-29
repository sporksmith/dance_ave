from django.conf.urls import patterns, url
import dance_ave.views as views

urlpatterns = patterns('',
    url(r'^$', views.Home.as_view(), name='home'),
)
