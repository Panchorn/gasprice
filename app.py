import os
import re
import time

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

already_broadcast = False


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
        try:
            gas_price_message = gasPriceService.get_gas_price()
            lineService.reply_msg(reply_token, gas_price_message)
        except Exception:
            print('Fail to get gas price')
            lineService.reply_msg(reply_token, 'มีบางอย่างผิดพลาด ลองใหม่อีกทีนะ')
    else:
        lineService.reply_msg(reply_token, 'ลองพิมพ์คำว่า \'ราคาน้ำมัน\' ดูนะ')


@app.route('/gas-price')
def get_gas_price():
    return gasPriceService.get_gas_price()


@scheduler.task('cron', id='gas_price_scheduler_task_1', second='0', minute='40', hour='16')
def gas_price_scheduler_task_1():
    global already_broadcast
    already_broadcast = False
    broadcast_until_success()


@scheduler.task('cron', id='gas_price_scheduler_task_2', second='0', minute='00', hour='17')
def gas_price_scheduler_task_2():
    broadcast_until_success()


@scheduler.task('cron', id='gas_price_scheduler_task_3', second='0', minute='20', hour='17')
def gas_price_scheduler_task_3():
    broadcast_until_success()


@scheduler.task('cron', id='gas_price_scheduler_task_4', second='0', minute='40', hour='17')
def gas_price_scheduler_task_4():
    broadcast_until_success()


@scheduler.task('cron', id='gas_price_scheduler_task_5', second='0', minute='00', hour='18')
def gas_price_scheduler_task_5():
    broadcast_until_success()


@scheduler.task('cron', id='gas_price_scheduler_task_6', second='0', minute='20', hour='18')
def gas_price_scheduler_task_6():
    broadcast_until_success()


def broadcast_until_success():
    global already_broadcast
    for _ in range(120):
        try:
            gas_price_message, is_price_change = gasPriceService.get_gas_price(check_price_change=True)
            if is_price_change and not already_broadcast:
                print('Broadcasting, price changed')
                lineService.broadcast_msg(gas_price_message)
                already_broadcast = True
            else:
                print('No broadcast, price not change')
        except Exception:
            print('Fail to get gas price')
            time.sleep(10)
        else:
            break


# @scheduler.task('interval', id='gas_price_scheduler_task', minutes=29, misfire_grace_time=900)
# def ping_task():
#     print('Hi I\'m working at ' + datetime.now().strftime("%d/%m/%Y %X"))
#     requests.get("https://namman.herokuapp.com/")


if __name__ == '__main__':
    app.run()
