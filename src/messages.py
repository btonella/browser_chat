
class Messages(object):
    messages = {
        0: [],
        1: []
    }
        
    def save_message(self, send_back, chat=0):
        if (not isinstance(send_back, list)):
            send_back = [send_back]

        for message in send_back:
            self.messages[chat].append(message)

        if (len(self.messages[chat]) > 50):
            self.messages[chat].pop(0)

    def get_messages(self, chat=0):
        return self.messages[chat]