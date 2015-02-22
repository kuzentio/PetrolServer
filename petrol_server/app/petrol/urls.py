from petrol_server.app.petrol import views
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout


urlpatterns = patterns('',
    url(r'^$', views.main),
    url(r'^upload_file/$', views.upload_file),

    (r'^accounts/login/$',  login),
    (r'^accounts/logout/$', logout),
)

