#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.forms import ModelForm
from datetime import datetime
from rapidsms.message import Message

class AWSUser(models.Model):
    aws_key = models.CharField(max_length=100, null=False)
    aws_secret = models.CharField(max_length=100,null=False)
    identifier = models.CharField(max_length=100,null=False)

    def __unicode__(self):
        return self.identifier

class MTurkConfig(models.Model):
    description = models.CharField(max_length=200)
    title = models.CharField(max_length=100)
    request = models.TextField()
    current = models.BooleanField(null=False, default=False)
    reward = models.DecimalField(max_digits=6,decimal_places=2)
    assignment_count = models.IntegerField()
    AWS_user = models.ForeignKey(AWSUser)

    @classmethod 
    def make_current(modelBase, config):
        for m in MTurkConfig.objects.all():
            m.current = False
            m.save()
        config.current = True

	

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = u'configuration'

class ConfigForm(ModelForm):
    class Meta:
        model = MTurkConfig
        #exclude['']

"""This is the model for translating incoming messages.
	It holds the sender's number, the time it was created,
	the original, the name of the translation method, an 
	optional translator id as well as an optional foreign key
	to another model"""

class Translation(models.Model):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    received_at = models.DateTimeField(default=datetime.now)
    orginal_message = models.TextField(null=False)
    translation_method = models.SlugField()
    translator_id = models.CharField(max_length=64, blank=True, null=True)
    instructions = generic.GenericForeignKey()
    translation = models.TextField(null=True, default=None)
    
    @classmethod
    def has_been_translated(self):
        return self.translation != None
