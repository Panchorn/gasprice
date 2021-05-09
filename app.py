import os
import requests
from flask import Flask, request, abort
import xmltodict
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
import re

from models.OilPrice import OilPrice
from services.handle_service import HandleService

app = Flask(__name__)

handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))
handle = HandleService()

url = 'https://www.bangchak.co.th/api/oilprice'
oil_list = {'E20', 'Gasohol 91', 'Gasohol 95'}


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    message = event.message.text
    is_match = re.search('ราคาน้ำมัน', message)
    if is_match:
        oil_price_message = get_oil_price(event)
        handle.reply_message(event, oil_price_message)


@app.route('/oil-price')
def get_oil_price():
    oil_price_raw = get_today_price()
    items = oil_price_raw['header']['item']

    filtered_items = filter_oil_type(items)
    # print(json.dumps(filtered_items))
    return print_response(filtered_items, oil_price_raw)


def get_today_price():
    response = requests.get(url)
    return xmltodict.parse(response.content)


def filter_oil_type(items):
    filtered = []
    for item in items:
        for oil_type in oil_list:
            if oil_type in item['type']:
                mapped_item = mapping_oil_price_response(oil_type, item)
                filtered.append(mapped_item.__dict__)
    return filtered


def mapping_oil_price_response(oil_type, oil_price):
    return OilPrice(
        oil_type,
        float(oil_price['today']),
        float(oil_price['tomorrow']),
        float(oil_price['tomorrow']) - float(oil_price['today']),
    )


def print_response(filtered_items, oil_price_raw):
    update_date = oil_price_raw['header']['update_date']
    remark_th = oil_price_raw['header']['remark_th']
    part_1 = "ราคาน้ำมันวันที่ " + update_date
    part_2 = ""
    for item in filtered_items:
        part_2 = part_2 + "\n\n" + item['name'] + "\n" + \
                 "วันนี้ " + str(item['today_price']) + " บาท\n" + \
                 "พรุ่งนี้ " + str(item['tomorrow_price']) + " บาท\n"
        if item['diff'] > 0.0:
            part_2 = part_2 + "น้ำมัน `ขึ้น` ราคา *" + str(item['diff']) + "* บาท\n"
        elif item['diff'] < 0.0:
            part_2 = part_2 + "น้ำมัน `ลด` ราคา *" + str(item['diff']) + "* บาท\n"
    part_3 = "\n\n" + remark_th.split("*")[-1]
    return part_1 + part_2 + part_3


if __name__ == '__main__':
    app.run()
