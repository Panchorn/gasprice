from linebot import LineBotApi
from linebot.models import TextSendMessage


class LineService:

    def __init__(self, channel_access_token):
        self.line_bot_api = LineBotApi(channel_access_token)

    def reply_msg(self, reply_token, msg):
        self.line_bot_api.reply_message(
            reply_token,
            [
                TextSendMessage(
                    text=msg,
                    quick_reply=default_quick_reply_item
                )
            ]
        )

    def push_msg(self, user_id, msg):
        self.line_bot_api.push_message(
            to=user_id,
            messages=[
                TextSendMessage(
                    text=msg,
                    quick_reply=default_quick_reply_item
                )
            ]
        )

    def broadcast_msg(self, msg):
        self.line_bot_api.broadcast(
            [
                TextSendMessage(
                    text=msg,
                    quick_reply=default_quick_reply_item
                )
            ]
        )


default_quick_reply_item = {
    'items': [
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

# Reference sticker list
# https://developers.line.biz/media/messaging-api/sticker_list.pdf
# https://devdocs.line.me/files/sticker_list.pdf
