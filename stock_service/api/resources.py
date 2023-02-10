# encoding: utf-8

from flask import request
from flask_restful import Resource
from stock_service.api.schemas import StockSchema
import requests
import csv, io, datetime

class StockResource(Resource):
    """
    Endpoint that is in charge of aggregating the stock information from external sources and returning
    them to our main API service. Currently we only get the data from a single external source:
    the stooq API.
    """

    def get(self):
        stock = list(request.values)[0]
        r = requests.get('https://stooq.com/q/l/?s=' + stock + '&f=sd2t2ohlcvn&h&e=csv').content
        r = r.decode('utf8')
        reader = csv.DictReader(io.StringIO(r))
        stock_data_obj = list(reader)[0]
        stock_data_obj = {k.lower(): v for k, v in stock_data_obj.items()}

        stock_data_obj['date'] = datetime.datetime.strptime(stock_data_obj['date'], "%Y-%m-%d")
        stock_data_obj['time'] = datetime.datetime.strptime(stock_data_obj['time'], "%H:%M:%S").time()

        schema = StockSchema()
        return schema.dump(stock_data_obj)
