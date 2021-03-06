import rapidsms
from models import *
from datetime import datetime

class App (rapidsms.app.App):
    def start (self):
        """Configure your app in the start phase."""
        pass

    def parse (self, message):
        """Parse and annotate messages in the parse phase."""
        pass
      
    def handle (self, message):
        """Register the respondent if the number is new."""
        if message.connection.identity == "15037849133" and message.text == "go":
            current_question = Question.objects.filter(current=True)
            if current_question:
                for respondent in Respondent.objects.all():
                    be = self.router.get_backend(respondent.connection.backend.slug)
                    be.message(respondent.phone_number, current_question[0].text).send()
                message.respond("current question sent out: %s" % current_question[0].text)
            else:
                message.respond("No current question")
            
        else:    
            before = datetime.now()
            respondent = Respondent.register_from_message(message)
            
            current_question = Question.objects.filter(current=1)
            
            if current_question:
                if current_question[0].not_yet_answered_by(respondent):
                    resp = Response(
                    question=current_question[0],
                    respondent=respondent,
                    text=message.text,
                    created_at=datetime.now()
                    )
                    resp.save()
                
                    if respondent.registered_at < before:
                        message.respond("Thanks for your reply! Your free minutes should arrive shortly.")
                    else:
                        message.respond("Thanks for your reply and for registering for Infone. Your free minutes should arrive shortly. Your Infone ID is: %d" % respondent.id)
                else:
                    message.respond("We already got your answer to this question earlier, thanks.")
                        
            else:
                if respondent.registered_at < before:
                    message.respond("You're already registered")
                else:
                    message.respond("Thanks for registering, %s. Welcome to Infone!" % respondent.reporter.full_name())
            
            # Respondent.objects.all().delete()
            #         Response.objects.all().delete()
            #         Question.objects.all().delete()

        
        pass

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
