from django.db import models

class Respondant(models.Model):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    registered_at = models.DateTimeField(null=True)

class Question(models.Model):
    text = models.CharField(max_length=160)
    created_at = models.DateTimeField(null=True)
    current = models.BooleanField(null=False, default=False)