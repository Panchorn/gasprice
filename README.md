# Oil Price

## General
This project attempt to send you the oil price by Line and notify you when it has changed.

Although you haven't a bot in friend list, you still get the information by call this API
> https://namman.herokuapp.com/oil-price

### Prerequisite
1. Set up virtual env and install library by pip
2. (Optional) Set local env variable for line bot channel 
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

### Get oil price information
```
    $ curl http://127.0.0.1:5000/oil-price
```

---

Thanks `Bangchak Corporation Public Company Limited` to provide the API
> https://www.bangchak.co.th/api/oilprice
