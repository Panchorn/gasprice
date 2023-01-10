# Gas Price

### General
This project attempt to send you the gas price by Line and notify you when it has changed.

Although you haven't a bot in friend list, you still get the information by call this API
> https://namman.onrender.com/gas-price

Focus on 3 types of gas (personal attention)
1. E20
2. Gasohol 91
3. Gasohol 95

---

### Prerequisite
1. Set up virtual env and install library by pip
2. Set local env variable for application
```
$ export FLASK_DEBUG=true
```
3. (Optional) Set local env variable for line bot channel 
   (if you have no bot yet, [create one](https://developers.line.biz/en/docs/line-developers-console/overview/#provider))
```
$ export CHANNEL_ACCESS_TOKEN='blah bla bla'
$ export CHANNEL_SECRET='blah bla bla'
```

### Start the service on your machine
```
$ flask run
or
$ python app.py
```

### Get gas price information
```
$ curl http://127.0.0.1:8000/gas-price
```

### Start the service on Render
```
$ gunicorn app:app --preload
```

---

### Example response
```text
ราคาน้ำมันวันที่ 10/01/2023

Gasohol E20
วันนี้ 32.54 บาท

Gasohol 91
วันนี้ 34.18 บาท

Gasohol 95
วันนี้ 34.45 บาท

ราคามีผล ณ วันที่ 7 ม.ค. 66 เวลา 05:00 น.
```
```text
ราคาน้ำมันวันที่ 10/01/2023

Gasohol E20
วันนี้ 32.54 บาท
พรุ่งนี้ 33.54 บาท
น้ำมัน ขึ้น ราคา 1.0 บาท

Gasohol 91
วันนี้ 34.18 บาท
พรุ่งนี้ 35.18 บาท
น้ำมัน ขึ้น ราคา 1.0 บาท

Gasohol 95
วันนี้ 34.45 บาท
พรุ่งนี้ 35.45 บาท
น้ำมัน ขึ้น ราคา 1.0 บาท

ราคามีผล ณ วันที่ 7 ม.ค. 66 เวลา 05:00 น.
```

---

Thanks `Bangchak Corporation Public Company Limited` to provide the API
> https://www.bangchak.co.th/api/oilprice
