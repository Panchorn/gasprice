import os
import re
from flask import Flask, request, abort
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from services.handle_service import HandleWebhookService
from services.oil_price_service import OilPriceService

app = Flask(__name__)

webhookHandler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))
handleWebhookService = HandleWebhookService()
oilPriceService = OilPriceService()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        webhookHandler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@webhookHandler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    message = event.message.text
    is_match = re.search('ราคาน้ำมัน', message)
    if is_match:
        oil_price_message = get_oil_price()
        handleWebhookService.reply_message(event, oil_price_message)
    else:
        handleWebhookService.reply_message(event, 'ลองพิมพ์คำว่า \'ราคาน้ำมัน\' ดูนะ')


@app.route('/oil-price')
def get_oil_price():
    return oilPriceService.get_oil_price()


if __name__ == '__main__':
    app.run()
