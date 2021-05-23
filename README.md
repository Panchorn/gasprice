# Gas Price

### General
This project attempt to send you the gas price by Line and notify you when it has changed.

Although you haven't a bot in friend list, you still get the information by call this API
> https://namman.herokuapp.com/gas-price

Focus on 3 types of gas (personal attention)
1. E20
2. Gasohol 91
3. Gasohol 95

### Prerequisite
1. Set up virtual env and install library by pip
2. Set local env variable for application
```
$ export FLASK_ENV=development
```
3. (Optional) Set local env variable for line bot channel 
   (if you have no bot yet, [create one](https://developers.line.biz/en/docs/line-developers-console/overview/#provider))
```
$ export CHANNEL_ACCESS_TOKEN='blah bla bla'
$ export CHANNEL_SECRET='blah bla bla'
```

### Start app on your machine
```
$ flask run
or
$ python app.py
```

### Get gas price information
```
$ curl http://127.0.0.1:5000/gas-price
```

### Example response
```text
ราคาน้ำมันวันที่ 10/05/2021

E20
วันนี้ 26.24 บาท

Gasohol 91
วันนี้ 27.48 บาท

Gasohol 95
วันนี้ 27.75 บาท

ราคามีผล ณ วันที่ 7 พ.ค. 64  เวลา 5.00 น.
```
```text
ราคาน้ำมันวันที่ 10/05/2021

E20
วันนี้ 26.24 บาท
พรุ่งนี้ 27.24 บาท
น้ำมัน ขึ้น ราคา 1.0 บาท

Gasohol 91
วันนี้ 27.48 บาท
พรุ่งนี้ 28.48 บาท
น้ำมัน ขึ้น ราคา 1.0 บาท

Gasohol 95
วันนี้ 27.75 บาท
พรุ่งนี้ 28.75 บาท
น้ำมัน ขึ้น ราคา 1.0 บาท

ราคามีผล ณ วันที่ 7 พ.ค. 64  เวลา 5.00 น.
```

---

Thanks `Bangchak Corporation Public Company Limited` to provide the API
> https://www.bangchak.co.th/api/oilprice


---

Using `Kaffeine` pings this app every 30 minutes to prevent slepp 
http://kaffeine.herokuapp.com/
