import os
import re
import requests

from datetime import datetime
from flask import Flask, request, abort
from flask_apscheduler import APScheduler
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from services.line_service import LineService
from services.gas_price_service import GasPriceService

app = Flask(__name__)

webhookHandler = WebhookHandler(os.getenv('CHANNEL_SECRET', ''))
lineService = LineService(os.getenv('CHANNEL_ACCESS_TOKEN', ''))
gasPriceService = GasPriceService()

# Scheduler config
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


@app.route('/')
def hello_world():
    print('Hi I\'m working at ' + datetime.now().strftime("%d/%m/%Y %X"))
    return 'Hello World'


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
        gas_price_message = gasPriceService.get_gas_price()
        lineService.reply_msg(reply_token, gas_price_message)
    else:
        lineService.reply_msg(reply_token, 'ลองพิมพ์คำว่า \'ราคาน้ำมัน\' ดูนะ')


@app.route('/gas-price')
def get_gas_price():
    return gasPriceService.get_gas_price()


@scheduler.task('cron', id='gas_price_scheduler_task', second='0', minute='30', hour='16')
def gas_price_scheduler_task():
    gas_price_message, is_price_change = gasPriceService.get_gas_price(check_price_change=True)
    if is_price_change:
        print('Broadcasting at 16:30:00 everyday when price change')
        lineService.broadcast_msg(gas_price_message)
    else:
        print('No broadcast, price not change')


# @scheduler.task('interval', id='gas_price_scheduler_task', minutes=29, misfire_grace_time=900)
# def ping_task():
#     print('Hi I\'m working at ' + datetime.now().strftime("%d/%m/%Y %X"))
#     requests.get("https://namman.herokuapp.com/")


if __name__ == '__main__':
    app.run()
