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
        
    text = models.CharField(max_length=160)
    created_at = models.DateTimeField(null=True)
    current = models.BooleanField(null=False, default=False)
    