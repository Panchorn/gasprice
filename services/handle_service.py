import os
from line_service import LineService
from linebot.models import TextSendMessage


class HandleService:

    def __init__(self):
        self.line = LineService(os.environ.get('CHANNEL_ID'))

    def reply_message(self, event, message):
        self.line.reply_msg(event.reply_token,
                            [
                                TextSendMessage(text=message)
                            ])
