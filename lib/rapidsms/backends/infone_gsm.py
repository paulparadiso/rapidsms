
#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

import time
import pygsm
import Queue

from rapidsms.message import Message
from rapidsms.connection import Connection
from rapidsms.backends import Backend
import backend
from rapidsms import log
from rapidsms import utils

from apps.infone.models import *

POLL_INTERVAL=2 # num secs to wait between checking for inbound texts
LOG_LEVEL_MAP = {
    'traffic':'info',
    'read':'info',
    'write':'info',
    'debug':'debug',
    'warn':'warning',
    'error':'error'
}

class Backend(Backend):
    _title = "pyGSM"
    
    def _log(self, modem, msg, level):
        # convert GsmModem levels to levels understood by
        # the rapidsms logger
        level = LOG_LEVEL_MAP[level]
        
        if self.modem_logger is not None:
            self.modem_logger.write(self,level,msg)
        else:
            self.router.log(level, msg)

    def configure(self, *args, **kwargs):
        self.modem = None
        self.modem_args = args

        # Variable to determine if question is currently going out
        self.is_polling = False

        # Variable to hold current question
        self.current_question = None

        # Variable to hold respondent to be polled
        self.current_respondent = 0

        # Variable to hold respondent list
        self.respondent_list = []

        # set max outbound text size
        if 'max_csm' in kwargs:
            self.max_csm = int(kwargs['max_csm'])
        else:
            self.max_csm = 1
        
        if self.max_csm>255:
            self.max_csm = 255
        if self.max_csm<1:
                self.max_csm = 1
                
        # make a modem log
        self.modem_logger = None
        if 'modem_log' in  kwargs:
            mlog = kwargs.pop('modem_log')
            level='info'
            if 'modem_log_level' in kwargs:
                level=kwargs.pop('modem_log_level')
            self.modem_logger = log.Logger(level=level, file=mlog, channel='pygsm')
            
        kwargs['logger'] = self._log
        self.modem_kwargs = kwargs
       
    
    def __send_sms(self, message):
        try:
            self.modem.send_sms(
                str(message.connection.identity),
                message.text,
                max_messages=self.max_csm)
        except ValueError, err:
            # TODO: Pass this error info on to caller!
            self.error('Error sending message: %s' % err)

    def send_question(self, numb, mess):
        try:
            self.modem.send_sms(
                numb,
                mess,
                max_messages = self.max_csm)
        except ValueError, err:
            self.error('Error sending message: %s' %err)
    
    def print_gotcha(self):
        print "GOTCHA"
    
    def run(self):
        while self._running:

            # Check if there is question currently being polled or
            # if we should start a new one.
            
            if self.is_polling == True:
                # This get a list of all respondents and assumes
                # that they come in the same order each time.
                r = Respondent.objects.all()
                if self.current_respondent >= len(r):
                    # This turns off the question being asked
                    # Could probably be more elegant.  Like holding
                    # onto the id of the current question.
                    for q in Question.objects.all():
                        if q.current == 1:
                            q.current = 0
                            q.save()
                    self.is_polling = False
                    self.current_respondent = 0
                else:
                    #self.send_question(number, self.current_question)
                    c = Connection(self,r[self.current_respondent].phone_number)
                    m = Message(connection=c,
                                text=self.current_question
                                )
                    self.__send_sms(m)
                    self.current_respondent += 1
            else:
                for q in Question.objects.all():
                    if q.current == 1:
                        self.current_question = q.text
                        print "Setting up: " + self.current_question
                        self.is_polling = True
            
            # check for new messages
            msg = self.modem.next_message()

            if msg is not None:
                # we got an sms! create RapidSMS Connection and
                # Message objects, and hand it off to the router
                c = Connection(self, msg.sender)
                m = Message(
                            connection=c, 
                            text=msg.text,
                            date=utils.to_naive_utc_dt(msg.sent)
                            )
                self.router.send(m)
                # Delete the message from the phone
                self.delete_message()
            # process all outbound messages
            while True:
                try:
                    self.__send_sms(self._queue.get_nowait())
                except Queue.Empty:
                    # break out of while
                    break
                
            # poll for new messages
            # every POLL_INTERVAL seconds
            time.sleep(POLL_INTERVAL)
    
    def start(self):
        self.modem = pygsm.GsmModem(
            *self.modem_args,
            **self.modem_kwargs)

        # If we got the connection, call superclass to
        # start the run loop--it just sets self._running to True
        # and calls run.
        if self.modem is not None:
            backend.Backend.start(self)

    def stop(self):
        # call superclass to stop--sets self._running
        # to False so that the 'run' loop will exit cleanly.
        backend.Backend.stop(self)

        # disconnect from modem
        if self.modem is not None:
            self.modem.disconnect()

    def delete_message(self):
        # Delete message at first index in phone.  This is
        # a very unstable and needs to be replaced with one
        # that is more robust.
        if self.modem is not None:
            self.modem.query("AT+CMGD=1")



        
