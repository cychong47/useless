#!/usr/bin/env python3

from slack import WebClient
from slack.errors import SlackApiError
import os

class SlackChannel():

    def __init__(self, token, channel):
        self.token = token
        self.channel = channel

        # Create a slack client
        try:
            self.slack_client = WebClient(token=token)
        except:
            print("Fail to create instance")

        return None

    def send(self, message):
        return self.slack_client.chat_postMessage(channel=self.channel, text=message)


if __name__ == "__main__":
    sc = SlackChannel(os.environ['SLACK_API_TOKEN'], "jarvis")
    sc.send("test")
