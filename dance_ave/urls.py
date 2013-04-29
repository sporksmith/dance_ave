from django.conf.urls import patterns, url
import dance_ave.views as views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('',
    url(r'^$', csrf_exempt(views.Home.as_view()), name='home'),
)
