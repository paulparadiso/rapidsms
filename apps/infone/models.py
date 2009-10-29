from django.db import models

class Respondant(models.Model):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    registered_at = models.DateTimeField(null=True)

class Question(models.Model):
    @classmethod
    def make_current(modelBase, question):
        # this is extremely inefficent and stupid, but works
        for q in Question.objects.all():
            q.current = False
            q.save()
            
        question.current = True
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