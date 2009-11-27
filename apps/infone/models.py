from django.db import models
from django.db import connection
from reporters.models import PersistantConnection, PersistantBackend, Reporter
from datetime import datetime
from rapidsms.message import Message
#from rapidsms import Router

class Respondent(models.Model):
    phone_number  = models.CharField(max_length=20, blank=True, null=True)
    registered_at = models.DateTimeField(null=True)
    reporter      = models.ForeignKey(Reporter, null=True, blank=True)
    connection    = models.ForeignKey(PersistantConnection, null=True, blank=True)

    @classmethod
    def register_from_message(modelBase, message):
        potential_registrant = Respondent.objects.filter(phone_number=message.connection.identity)
        if potential_registrant:
            return potential_registrant[0]
        else:
            # have to create a Reporter and PersistentConnection
            # TODO: 
            spl = message.text.partition(" ")
            
            reporter = Reporter(alias=message.connection.identity, first_name=spl[0], last_name=spl[2])
            reporter.save()
            
            be = PersistantBackend.from_message(message)
            be.save()
            
            conn = PersistantConnection.from_message(message)
            conn.reporter = reporter
            conn.save()
            conn.seen()
            
            resp = Respondent(
            phone_number=message.connection.identity,
            registered_at=datetime.now(),
            reporter=reporter,
            connection=conn)
            resp.save()
            
            return resp

class Question(models.Model):
    @classmethod
    def make_current(modelBase, question):
        # this is extremely inefficent and stupid, but works
        for q in Question.objects.all():
            q.current = False
            q.save()
            
        question.current = True
        #router = Router()
        #router.add_backend("http_HttpHandler")
        #be = router.get_backend("http_HttpHandler")
        #be.message("5037849133", "blah").send()
        # resp = Respondant.objects.all()[0]
        # Message(resp.connection, question.text).send()
        # for respondant in Respondant.objects.all():
            # respondant.connection.backend.message(respondant.phone_number, question.text).send()
        # for respondent in Respondent.objects.all():
            # respondent.connection.backend.message(respondent.phone_number, question.text).send()

        question.save()
    
    def not_yet_answered_by(self, respondent):
        return Response.objects.filter(question=self, respondent=respondent).count() == 0

    text = models.CharField(max_length=160)
    created_at = models.DateTimeField(null=True)
    current = models.BooleanField(null=False, default=False)
    
class Response(models.Model):
    question = models.ForeignKey(Question)
    respondent = models.ForeignKey(Respondent)
    text = models.CharField(max_length=160)
    created_at = models.DateTimeField(null=True)

class Target(models.Model):
    question = models.ForeignKey(Question)
    respondent = models.ForeignKey(Respondent)
    response = models.ForeignKey(Response)
    sent_at = models.DateTimeField(null=True)
