from petrol_server.app.petrol import views
from django.conf.urls import patterns, url
from django.contrib.auth.views import login


urlpatterns = patterns('',
    url(r'^$', views.main),
    url(r'^balance/(?P<company_id>\d+)/$', views.balance),
    url(r'^statistic', views.statistic),

    (r'^accounts/login/$',  login),
    (r'^accounts/logout/$', views.logout_view),
    (r'^logout/$', views.logout_view),


)

