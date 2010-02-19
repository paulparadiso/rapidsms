from rapidsms.webui.utils import render_to_response
from models import *
from datetime import datetime, timedelta
from django import forms
from django.http import HttpResponseRedirect
from django.http import HttpResponse

class ConfigForm(forms.Form):
    text = forms.CharField(max_length=160, widget=forms.widgets.Textarea())
    current = forms.BooleanField(required=False)

def config(req):
    template_path = "xtrans/config.html"
    form = ConfigForm()
    return render_to_response(req, template_path, {'form' : form})

def config_submit(req):
    template_path = "xtrans/config_submit.html"
    return render_to_response(req, template_path, {})

def app_index(req):
    template_path = "xtrans/index.html"
    return render_to_response(req, template_path, {})
