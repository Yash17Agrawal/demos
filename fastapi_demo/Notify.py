class Notify:
    def __init__(self):
        # Initialize the sdk with creds
        pass

    def _send_email(self, message):
        pass
    
    def _print(self, message):
        print(message)

    def send_notification(self, message):
        self._print(message)
        # uncomment to change the mode of notification
        # self._send_email(message)

