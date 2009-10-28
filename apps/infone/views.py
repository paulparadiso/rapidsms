from rapidsms.webui.utils import render_to_response
from models import *
from datetime import datetime, timedelta
from django import forms

class QuestionForm(forms.Form):
    text = forms.CharField(max_length=160, widget=forms.widgets.Textarea())
    current = forms.BooleanField(required=False)

def respondants_index(req):
    template_path = "infone/respondants/index.html"
    all = Respondant.objects.order_by('registered_at').reverse()
    return render_to_response(req, template_path, {'respondants' : all})

def app_index(req):
    template_path = "infone/index.html"
    return render_to_response(req, template_path, {})

def new_question(req):
    template_path = "infone/questions/new.html"
    form = QuestionForm()
    return render_to_response(req, template_path, {'form' : form})
    
def create_question(req):
    template_path = "infone/questions/index.html"
    
    success = False
    
    if req.method == 'POST': # If the form has been submitted...
        form = QuestionForm(req.POST) # A form bound to the POST data
        if form.is_valid():
            question = Question(
            text=form.cleaned_data['text'],
            current=form.cleaned_data['current'],
            created_at=datetime.now())
            question.save()
            
            success = True
            
        else:
            return HttpResponseRedirect('/infone/questions/new')
    
    all = Question.objects.order_by('created_at').reverse()
    return render_to_response(req, template_path, {'questions' : all, 'success' : success})