#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from rapidsms.webui.utils import render_to_response
from models import *
from datetime import datetime, timedelta
from django import forms
from django.http import HttpResponseRedirect
from django.http import HttpResponse

def config(req):
    template_path = "xtrans/config.html"
    form = ConfigForm()
    return render_to_response(req, template_path, {'form' : form})

def config_submit(req):
    template_path = "xtrans/config_submit.html"
    return render_to_response(req, template_path, {})

def app_index(req):
	current_method = get_current_method()
	all_methods = get_all_methods()
	template_path = "xtrans/index.html"
	return render_to_response(req, template_path, {})

def create_config(req):
	c = MTurkConfig()
	f = ConfigForm(instance=c)
	template_path = "xtrans/mturk_config.html"
	return render_to_response(req, template_path, {'form':f})

def get_current_method():
	return 'holder'
	
def get_all_methods():
	return 'holder'
	