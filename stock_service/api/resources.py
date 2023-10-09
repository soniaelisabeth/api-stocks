# encoding: utf-8
import csv
import json
import requests
from io import StringIO
from flask_restful import Resource, reqparse

from api_service.sqlite_util import execute_query

requests_data = {}

class StockResource(Resource):
    """
    Endpoint that is in charge of aggregating the stock information from external sources and returning
    them to our main API service. Currently, we only get the data from a single external source:
    the stooq API.
    """
    MAIN_URL = 'https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcvn&h&e=csv'

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('query', type=str, required=True, help='Stock code is required')
        super(StockResource, self).__init__()
    
    def get(self):
        args = self.parser.parse_args()
        query_param = args['query']
        url = self.MAIN_URL.format(stock_code=query_param)
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                stock_data = self.format_request(stock_data=response.text)
                db_result = self.save_to_database(stock_data=stock_data)
                if db_result != True:
                    return db_result
                
                return self.format_request_return_information(stock_data=stock_data)
            else:
                return {'error': f'Failed to fetch data. Status code: {response.status_code}'}, 500

        except requests.exceptions.RequestException as e:
            return {'error': f'Request failed: {str(e)}'}, 500

    def format_request(self, stock_data):
        csv_reader = csv.DictReader(StringIO(stock_data))
        csv_list = [row for row in csv_reader]
        stock_data_formatted = [{key.lower(): value for key, value in row.items()} for row in csv_list][0]
        return stock_data_formatted
    
    def save_to_database(self, stock_data):
        query = 'INSERT OR REPLACE INTO stocks (name, data) VALUES (?,?)'
        name = stock_data.get('name', 'UnamedStock')
        stock_data = self.update_stock_requests_data(stock_data, name)
        values = (name, json.dumps(stock_data))
        return execute_query(query, values)

    def format_request_return_information(self, stock_data):
        return {
            "symbol": stock_data.get('symbol', None),
            "company_name": stock_data.get('name', 'UnamedStock'),
            "quote": stock_data.get('close', None),
        }
    
    def update_stock_requests_data(self, stock_data, name):
        if name not in requests_data.keys():
            requests_data[name] = 1
        else:
            requests_data[name] += 1
        stock_data['times_requested'] = requests_data[name]
        return stock_data
            