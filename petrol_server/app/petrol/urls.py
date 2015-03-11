from django.contrib import admin
from django.views.generic import RedirectView
from petrol_server.app.petrol import views
from django.conf.urls import patterns, url, include
from django.contrib.auth.views import login, logout


urlpatterns = patterns('',
    url(r'^$', views.main),

    (r'^accounts/login/$',  login),
    (r'^accounts/logout/$', logout),
    (r'^logout/$', views.logout_view),

)

