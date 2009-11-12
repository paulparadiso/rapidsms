from rapidsms.webui.utils import render_to_response
from models import *
from datetime import datetime, timedelta
from django import forms
from django.http import HttpResponseRedirect
from django.http import HttpResponse

import csv

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

def question_csv(req, id):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = "attachment; filename=infone_response_q%s.csv" % id 

    writer = csv.writer(response)
    question = Question.objects.get(id=id)
    responses = question.response_set.all()
    writer.writerow(['Respondant', 'Response', 'Received At'])

    for r in responses:
        writer.writerow([r.respondant.phone_number, r.text, r.created_at])

    return response

def new_question(req):
    template_path = "infone/questions/new.html"
    form = QuestionForm()
    return render_to_response(req, template_path, {'form' : form})

def edit_question(req, id):
    template_path = "infone/questions/edit.html"
    question = Question.objects.get(id=id)
    # this is stupid but necessary:
    current = True if question.current == 1 else False
    form = QuestionForm({'text' : question.text, 'current' : current})
    return render_to_response(req, template_path, {'question' : question, 'form' : form})
    
def edit_question(req, id):
    template_path = "infone/questions/edit.html"
    question = Question.objects.get(id=id)
    # this is stupid but necessary:
    current = True if question.current == 1 else False
    form = QuestionForm({'text' : question.text, 'current' : current})
    return render_to_response(req, template_path, {'question' : question, 'form' : form})

def update_question(req, id):    
    if req.method == 'POST': # If the form has been submitted...
        success = False
        
        form = QuestionForm(req.POST) # A form bound to the POST data
        if form.is_valid():
            question = Question.objects.get(id=id)
            question.text = form.cleaned_data['text']
            question.current = form.cleaned_data['current']
            question.save()
                                    
            if form.cleaned_data['current'] == 1:
                Question.make_current(question)
            
            success = True
            
        else:
            return HttpResponseRedirect('/infone/questions/' + question.id)
            
    else:   
        template_path = "infone/questions/show.html"
        question = Question.objects.get(id=id)
        responses = question.response_set.all()
        return render_to_response(req, template_path, {'question' : question, 'responses' : responses})
       
    return HttpResponseRedirect('/infone/questions')

def create_question(req):
    template_path = "infone/questions/index.html"
    
    success = False
    
    if req.method == 'POST': # If the form has been submitted...
        form = QuestionForm(req.POST) # A form bound to the POST data
        if form.is_valid():
            question = Question(
            text=form.cleaned_data['text'],
            created_at=datetime.now())
            question.save()
                        
            if form.cleaned_data['current'] == 1:
                Question.make_current(question)
            
            success = True
            
        else:
            return HttpResponseRedirect('/infone/questions/new')
    
    all = Question.objects.order_by('created_at').reverse()
    return render_to_response(req, template_path, {'questions' : all, 'success' : success})