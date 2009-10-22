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
        """Register the respondant if the number is new."""            
        exists = Respondant.objects.filter(phone_number=message.connection.identity)
        
        if exists:
            message.respond("We've already got your number. You're good.")
        else:
            resp = Respondant(
            phone_number=message.connection.identity,
            registered_at=datetime.now())
            resp.save()
            message.respond("Thanks for registering! Your infone ID is: %d" % resp.id)

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
