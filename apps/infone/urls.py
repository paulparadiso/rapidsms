#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import os
from django.conf.urls.defaults import *
import infone.views as views

urlpatterns = patterns('',
    url(r'^infone/respondants/?$', views.respondants_index),
    url(r'^infone/?$', views.app_index),
    url(r'^infone/questions/new?$', views.new_question),
    url(r'^infone/questions/?$', views.create_question),
    url(r'^infone/questions/(?P<id>\d+)/edit/?$', views.edit_question),
    url(r'^infone/questions/(?P<id>\d+)/?$', views.update_question)
)
