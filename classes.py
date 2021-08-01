class User:
    def __init__(self, update):
        try:
            self.id = update.message.chat_id
            self.name = update.message.from_user.first_name
            self.text = update.message.text
        except Exception:
            self.id = update.callback_query.from_user.id
            self.name = update.callback_query.from_user.first_name
            self.text = update.message.text
        try:
            self.number = update.message.contact.phone_number
        except Exception:
            pass
        # class SuperUser():
        #     def __init__(self):

