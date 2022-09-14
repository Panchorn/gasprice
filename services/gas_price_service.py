import json
from datetime import datetime

import requests
import xmltodict

from models.GasPrice import GasPrice


class GasPriceService:

    def __init__(self):
        self.url = 'https://www.bangchak.co.th/api/oilprice'
        self.ping_url = 'https://namman.onrender.com'
        self.gas_list = {'E20', 'Gasohol 91', 'Gasohol 95'}

    def ping(self):
        requests.get(self.ping_url)

    def get_gas_price(self, check_price_change=False):
        gas_price_raw = self.get_bangchak_price()
        items = gas_price_raw['header']['item']

        filtered_items = self.filter_gas_type(items)
        print(json.dumps(filtered_items))
        gas_price_message, is_price_change = self.build_response(filtered_items, gas_price_raw)
        if check_price_change:
            return gas_price_message, is_price_change
        else:
            return gas_price_message

    def get_bangchak_price(self):
        response = requests.get(self.url)
        return xmltodict.parse(response.content)

    def filter_gas_type(self, items):
        filtered = []
        for item in items:
            for gas_type in self.gas_list:
                if gas_type in item['type']:
                    mapped_item = self.mapping_gas_price_response(gas_type, item)
                    filtered.append(mapped_item.__dict__)
        return filtered

    @staticmethod
    def mapping_gas_price_response(gas_type, gas_price):
        return GasPrice(
            gas_type,
            float(gas_price['today']),
            float(gas_price['tomorrow']),
            round(float(gas_price['tomorrow']) - float(gas_price['today']), 2),
        )

    @staticmethod
    def build_response(filtered_items, gas_price_raw):
        is_price_change = False
        remark_th = gas_price_raw['header']['remark_th']
        now = datetime.now()
        part_1 = "ราคาน้ำมันวันที่ " + now.strftime("%d/%m/%Y")
        part_2 = ""
        for item in filtered_items:
            part_2 = part_2 + "\n\n" + item['name'] + "\n" + \
                     "วันนี้ " + str(item['today_price']) + " บาท"
            tmr_price = "\nพรุ่งนี้ " + str(item['tomorrow_price']) + " บาท\n"
            if item['diff'] > 0.0:
                part_2 = part_2 + tmr_price + "น้ำมัน ขึ้น ราคา " + str(item['diff']) + " บาท"
                is_price_change = True
            elif item['diff'] < 0.0:
                part_2 = part_2 + tmr_price + "น้ำมัน ลด ราคา " + str(item['diff']) + " บาท"
                is_price_change = True
        part_3 = "\n\n" + remark_th.split("*")[-1]
        return part_1 + part_2 + part_3, is_price_change
