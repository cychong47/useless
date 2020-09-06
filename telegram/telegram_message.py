#!/bin/env python3
import telegram
import sys
import time

class TelegramChannel():
    def __init__(self, token):
        try:
            self.bot = telegram.Bot(token=token)
        except:
            print("fail to get token. just exit")
            sys.exit(0)

    def send_msg(self, msg):
        #updates = bot.getUpdates()
        try:
            self.bot.deleteWebhook()
            chat_id = self.bot.getUpdates()[-1].message.chat.id
            self.bot.sendMessage(chat_id=chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)
        except:
            pass

    def get_update(self):
        return self.bot.getUpdates()

if __name__ == "__main__":
    tc = TelegramChannel("")

    while True:
        updates = tc.getUpdates()
        time.sleep(1)
