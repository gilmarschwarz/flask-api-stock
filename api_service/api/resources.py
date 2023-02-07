from flask import request, session
from flask_restful import Resource
from api_service.api.schemas import StockInfoSchema, StockHistorySchema, StockStatsSchema
from api_service.extensions import db
from api_service.models import UserHistory
from api_service.auth.helpers import auth
from sqlalchemy import func
import requests
import datetime

class StockQuery(Resource):
    """
    Endpoint to allow users to query stocks
    """

    @auth.login_required
    def get(self):
        # TODO: Call the stock service, save the response, and return the response to the user in
        # the format dictated by the StockInfoSchema.

        stock = list(request.values)[0]
        data_from_service = requests.get('http://127.0.0.1:5001/api/v1/stock?' + stock)

        if data_from_service.status_code != 200:
            return {'error': 'Something went wrong, try to check your stock parameter'}

        data_from_service = data_from_service.json()

        data_to_save = data_from_service.copy()
        data_to_save['date_hist'] = datetime.datetime.strptime(data_to_save['date'] + " " + data_to_save['time'], "%Y-%m-%d %H:%M:%S")
        data_to_save.pop('time')
        data_to_save.pop('date')
        data_to_save['id_user'] = session['id_user']

        hist = UserHistory(**data_to_save)
        db.session.add(hist)
        db.session.commit()

        data_from_service['company_name'] = data_from_service.pop('name')
        data_from_service['quote'] = data_from_service.pop('close')
        schema = StockInfoSchema()
        return schema.dump(data_from_service)


class History(Resource):
    """
    Returns queries made by current user.
    """
    @auth.login_required
    def get(self):
        hist = UserHistory.query.filter_by(id_user=session['id_user']).all()
        schema = StockHistorySchema(many=True)
        return schema.dump(hist)


class Stats(Resource):
    """
    Allows admin users to see which are the most queried stocks.
    """
    @auth.login_required
    def get(self):
        if not session['check_admin']:
            return {'error': 'Only Admins Access'}

        stock_lst = UserHistory.query.with_entities(UserHistory.symbol, func.count(UserHistory.symbol)).\
                                             group_by(UserHistory.symbol).\
                                             order_by(func.count(UserHistory.symbol).desc()).all()

        stock_lst_dic = []
        for stock in stock_lst:
            stock_lst_dic.append({'stock': stock[0], 'times_requested': stock[1]})

        del stock_lst
        schema = StockStatsSchema(many=True)
        return schema.dump(stock_lst_dic)