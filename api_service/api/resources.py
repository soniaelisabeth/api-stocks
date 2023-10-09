import json
from datetime import datetime
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token

from api_service.api.schemas import StockInfoSchema, StockInfoSchemaFull, StockInfoSchemaTimesRequested
from api_service.sqlite_util import select_query
from api_service.sqlite_util import is_user_available


class StockQuery(Resource): 
    """
    Endpoint to allow users to query stocks
    """
    @jwt_required()
    def get(self):
        # TODO: Call the stock service, save the response, and return the response to the user in
        # the format dictated by the StockInfoSchema.
        data_from_service = select_query()
        schema = StockInfoSchema()
        formatted_results = [
            schema.dump({
                "symbol": json.loads(data_json).get('symbol', None),
                "company_name": company_name,
                "quote": float(json.loads(data_json).get('close', None))
            }) for _, company_name, data_json in data_from_service
        ]

        return formatted_results


class History(Resource):
    """
    Returns queries made by current user.
    """
    @jwt_required()
    def get(self):
        # TODO: Implement this method.
        data_from_service = select_query()
        schema = StockInfoSchemaFull()
        formatted_results = [
            schema.dump({
                "date": datetime.strptime(
                    json.loads(data_json).get('date', '')+'T' + json.loads(data_json).get('time', '') +'Z', '%Y-%m-%dT%H:%M:%SZ'
                ),
                "name": json.loads(data_json).get('name', None),
                "symbol": json.loads(data_json).get('symbol', None),
                "open": float(json.loads(data_json).get('open', None)),
                "high": float(json.loads(data_json).get('high', None)),
                "low": float(json.loads(data_json).get('low', None)),
                "close": float(json.loads(data_json).get('close', None)),
            }) for _, _, data_json in data_from_service
        ]

        return formatted_results


class Stats(Resource):
    """
    Allows admin users to see which are the most queried stocks.
    """
    @jwt_required()
    def get(self):
        # TODO: Implement this method.
        data_from_service = select_query()
        schema = StockInfoSchemaTimesRequested()
        formatted_results = [
            schema.dump({
                "symbol": json.loads(data_json).get('symbol', None),
                "times_requested": int(json.loads(data_json).get('times_requested', None)),
            }) for _, _, data_json in data_from_service
        ]
        top_five_stocks = sorted(formatted_results, key=lambda x: x["times_requested"], reverse=True)[:5]
        return top_five_stocks
    
class Login(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True, help='Stock code is required')
        self.parser.add_argument('password', type=str, required=True, help='Stock code is required')
        super(Login, self).__init__()

    def get(self):
        args = self.parser.parse_args()
        username = args['username']
        password = args['password']
        if is_user_available(username, password):
            access_token = create_access_token(identity=username)
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401
