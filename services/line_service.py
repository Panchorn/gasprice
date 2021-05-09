from linebot import LineBotApi


class LineService:

    def __init__(self, channel_access_token):
        self.line_bot_api = LineBotApi(channel_access_token)

    def reply_msg(self, reply_token, messages):
        self.line_bot_api.reply_message(reply_token, messages)

    def push_msg(self, to, messages):
        self.line_bot_api.push_message(to, messages)

# Reference sticker list
# https://developers.line.biz/media/messaging-api/sticker_list.pdf
# https://devdocs.line.me/files/sticker_list.pdf
