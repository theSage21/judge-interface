from django.conf.urls import patterns, url


urlpatterns = patterns('contest.views',
                       url(r'^$', 'home', name='home'),
                       url(r'^register/$', 'register', name='register'),
                       )
