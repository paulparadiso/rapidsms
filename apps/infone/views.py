from rapidsms.webui.utils import render_to_response
from models import *
from datetime import datetime, timedelta

def respondants_index(req):
    template_path = "infone/respondants/index.html"
    all = Respondant.objects.order_by('registered_at').reverse()
    return render_to_response(req, template_path, {'respondants' : all})

def app_index(req):
    template_path = "infone/index.html"
    return render_to_response(req, template_path, {})
