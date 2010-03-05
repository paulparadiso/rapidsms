#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import os
from django.conf.urls.defaults import *
import xtrans.views as views

urlpatterns = patterns('',
                       url(r'^xtrans/?$',views.app_index),
                       url(r'^xtrans/config/?$',views.config),
                       url(r'^xtrans/config/create/?&', views.create_config),
                       url(r'^xtrans/config/submit/?$', views.create_config),
)
