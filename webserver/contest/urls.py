from django.conf.urls import patterns, url


urlpatterns = patterns('contest.views',
                       url(r'^$', 'home', name='home'),
                       url(r'^contest/(?P<pk>\d+)/$', 'manage', name='manage'),
                       url(r'^unauthorized/$', 'unauthorized', name='403'),
                       url(r'^register/$', 'register', name='register'),
                       )
