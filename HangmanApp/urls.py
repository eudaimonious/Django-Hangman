from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^anotherturn/$', views.anotherturn, name='anotherturn'),
    url(r'^endgame/$', views.endgame, name='endgame')
)
