from django.db import models

class Respondant(models.Model):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    registered_at = models.DateTimeField(null=True)
