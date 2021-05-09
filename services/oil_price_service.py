import json
from datetime import datetime

import requests
import xmltodict

from models.OilPrice import OilPrice


class OilPriceService:

    def __init__(self):
        self.url = 'https://www.bangchak.co.th/api/oilprice'
        self.oil_list = {'E20', 'Gasohol 91', 'Gasohol 95'}

    def get_oil_price(self):
        oil_price_raw = self.get_bangchak_price()
        items = oil_price_raw['header']['item']

        filtered_items = self.filter_oil_type(items)
        print(json.dumps(filtered_items))
        return self.print_response(filtered_items, oil_price_raw)

    def get_bangchak_price(self):
        response = requests.get(self.url)
        return xmltodict.parse(response.content)

    def filter_oil_type(self, items):
        filtered = []
        for item in items:
            for oil_type in self.oil_list:
                if oil_type in item['type']:
                    mapped_item = self.mapping_oil_price_response(oil_type, item)
                    filtered.append(mapped_item.__dict__)
        return filtered

    @staticmethod
    def mapping_oil_price_response(oil_type, oil_price):
        return OilPrice(
            oil_type,
            float(oil_price['today']),
            float(oil_price['tomorrow']),
            float(oil_price['tomorrow']) - float(oil_price['today']),
        )

    @staticmethod
    def print_response(filtered_items, oil_price_raw):
        remark_th = oil_price_raw['header']['remark_th']
        now = datetime.now()
        part_1 = "ราคาน้ำมันวันที่ " + now.strftime("%d/%m/%Y")
        part_2 = ""
        for item in filtered_items:
            part_2 = part_2 + "\n\n" + item['name'] + "\n" + \
                     "วันนี้ " + str(item['today_price']) + " บาท"
            tmr_price = "\nพรุ่งนี้ " + str(item['tomorrow_price']) + " บาท\n"
            if item['diff'] > 0.0:
                part_2 = part_2 + tmr_price + "น้ำมัน ขึ้น ราคา " + str(item['diff']) + " บาท"
            elif item['diff'] < 0.0:
                part_2 = part_2 + tmr_price + "น้ำมัน ลด ราคา " + str(item['diff']) + " บาท"
        part_3 = "\n\n" + remark_th.split("*")[-1]
        return part_1 + part_2 + part_3
