#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import rapidsms
from models import *
from datetime import datetime
import translators

class App (rapidsms.app.App):

	def start (self):
		"""Configure your app in the start phase."""
		#This is the default translation method from the tranlators.py file.
		self.method = translators.default
		pass
	
	def parse (self, message):
		"""Parse and annotate messages in the parse phase."""
		pass
	
	def handle (self, message):
		"""Add your main application logic in the handle phase."""
		if self.method != 'off':
			entry = Translation(
				phone_number = message.connection.identity,
				original_message = message.text,
				translation_method = self.method,
				
				
				)
			result = translate(entry)
			
	def cleanup (self, message):
		"""Perform any clean up after all handlers have run in the
		cleanup phase."""
		pass
	
	def outgoing (self, message):
		"""Handle outgoing message notifications."""
		pass
	
	def stop (self):
		"""Perform global app cleanup when the application is stopped."""
		pass

	def method(self):
		print "You Got Me"
		
	def translate(self,msg_id):
		if hasattr(self,self.method):
			return getattr(self,self.method)(msg_id)
		else:
			return "Method does not exist"
		
	def ajax_GET_transmethod(*args):
		print args
			
	"""These methods are the translation functions.
	They are called by name.  To add a new one simply add
	a method that takes an argument for the model id."""
		
	def mturk(self,msg_id):
		return 1
		
	def wwl(self,msg_id):
		return 1
		
	def meedan(self,msg_id):
		return 1
	
	def human(self,msg_id):
		return 1
	
