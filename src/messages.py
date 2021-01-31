
class Messages(object):
    messages = []
        
    def save_message(self, send_back):
        if (not isinstance(send_back, list)):
            send_back = [send_back]

        for message in send_back:
            self.messages.append(message)

        if (len(self.messages) > 50):
            self.messages.pop(0)

    def get_messages(self):
        return self.messages