import os
import re
from datetime import datetime

from flask import Flask, request, abort
from flask_apscheduler import APScheduler
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from services.line_service import LineService
from services.oil_price_service import OilPriceService

app = Flask(__name__)

webhookHandler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))
lineService = LineService(os.environ.get('CHANNEL_ACCESS_TOKEN'))
oilPriceService = OilPriceService()

# Scheduler config
scheduler = APScheduler()
# scheduler.start()


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
    reply_token = event.reply_token
    is_match = re.search('ราคาน้ำมัน', message)
    if is_match:
        oil_price_message = oilPriceService.get_oil_price()
        lineService.reply_msg(reply_token, oil_price_message)
    else:
        lineService.reply_msg(reply_token, 'ลองพิมพ์คำว่า \'ราคาน้ำมัน\' ดูนะ')


@app.route('/oil-price')
def get_oil_price():
    return oilPriceService.get_oil_price()


@scheduler.task('cron', id='oil_price_scheduler_task', second='0', minute='0', hour='11')
def oil_price_scheduler_task():
    oil_price_message, is_price_change = oilPriceService.get_oil_price(check_price_change=True)
    if is_price_change:
        print('Broadcasting at 11:00:00 everyday when price change')
        lineService.broadcast_msg(oil_price_message)
    else:
        print('No broadcast, price not change')


@scheduler.task('cron', id='test', second='0', minute='20', hour='1')
def test():
    print('test I\'m working every minute' + " at " + datetime.now().strftime("%X"))


@scheduler.task('cron', id='test2', second='*')
def test2():
    print('test2 I\'m working every minute' + " at " + datetime.now().strftime("%X"))


if __name__ == '__main__':
    app.run()
