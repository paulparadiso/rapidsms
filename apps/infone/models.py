from django.db import models
from django.db import connection
from reporters.models import PersistantConnection, PersistantBackend, Reporter
from datetime import datetime
from rapidsms.message import Message

class Respondant(models.Model):
    phone_number  = models.CharField(max_length=20, blank=True, null=True)
    registered_at = models.DateTimeField(null=True)
    reporter      = models.ForeignKey(Reporter, null=True, blank=True)
    connection    = models.ForeignKey(PersistantConnection, null=True, blank=True)

    @classmethod
    def register_from_message(modelBase, message):
        potential_registrant = Respondant.objects.filter(phone_number=message.connection.identity)
        if potential_registrant:
            return potential_registrant[0]
        else:
            # have to create a Reporter and PersistentConnection
            reporter = Reporter(alias=message.connection.identity)
            reporter.save()
            
            conn = PersistantConnection.from_message(message)
            conn.reporter = reporter
            conn.save()
            conn.seen()
            
            resp = Respondant(
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
        # resp = Respondant.objects.all()[0]
        # Message(resp.connection, question.text).send()
        # for respondant in Respondant.objects.all():
            # respondant.connection.backend.message(respondant.phone_number, question.text).send()

        question.save()
    
    def not_yet_answered_by(self, respondant):
        return Response.objects.filter(question=self, respondant=respondant).count() == 0

    text = models.CharField(max_length=160)
    created_at = models.DateTimeField(null=True)
    current = models.BooleanField(null=False, default=False)
    
class Response(models.Model):
    question = models.ForeignKey(Question)
    respondant = models.ForeignKey(Respondant)
    text = models.CharField(max_length=160)
    created_at = models.DateTimeField(null=True)
    
    # TODO: parsed_text? or something from method defined in question?