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

    def register(something_stupid, potential_registrant, message):
      """helper for registering the respondant if necessary. returns a saved respondant"""  
        
      if potential_registrant:
          return potential_registrant[0]
      else:
          resp = Respondant(
          phone_number=message.connection.identity,
          registered_at=datetime.now())
          resp.save()
          return resp
      
    def handle (self, message):
        """Register the respondant if the number is new."""

        potential_respondant = Respondant.objects.filter(phone_number=message.connection.identity)
        respondant = self.register(potential_respondant, message)
        
        current_question = Question.objects.filter(current=1)

        if current_question:
            if current_question[0].not_yet_answered_by(respondant):
                resp = Response(
                question=current_question[0],
                respondant=respondant,
                text=message.text,
                created_at=datetime.now()
                )
                resp.save()
            
                if potential_respondant:
                    message.respond("Thanks for your reply! Your free minutes should arrive shortly.")
                else:
                    message.respond("Thanks for your reply and for registering for Infone. Your free minutes should arrive shortly. Your Infone ID is: %d" % respondant.id)
            else:
                message.respond("We already got your answer to this question earlier, thanks.")
                    
        else:
            if potential_respondant:
                message.respond("You're already registered.")
            else:
                message.respond("Thanks for registering! Your Infone ID is: %d" % respondant.id)
        
        # Respondant.objects.all().delete()
        # Response.objects.all().delete()
        # Question.objects.all().delete()

        
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
