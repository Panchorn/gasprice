import os
from services.line_service import LineService
from linebot.models import TextSendMessage


class HandleWebhookService:

    def __init__(self):
        self.line = LineService(os.environ.get('CHANNEL_ACCESS_TOKEN'))

    def reply_message(self, event, message):
        self.line.reply_msg(event.reply_token,
                            [
                                TextSendMessage(
                                    text=message,
                                    quick_reply=
                                    {
                                        'items':
                                            [
                                                {
                                                    'type': 'action',
                                                    'action': {
                                                        'type': 'message',
                                                        'label': 'ราคาน้ำมันวันนี้',
                                                        'text': 'ราคาน้ำมัน'
                                                    }
                                                }
                                            ]
                                    }
                                )
                            ])
