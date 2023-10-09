# encoding: utf-8

from api_service.extensions import ma


class StockInfoSchema(ma.Schema):
    symbol = ma.String(dump_only=True)
    company_name = ma.String(dump_only=True)
    quote = ma.Float(dump_only=True)


class StockInfoSchemaFull(ma.Schema):
    date = ma.Date(dump_only=True)
    name = ma.String(dump_only=True)
    symbol = ma.String(dump_only=True)
    open = ma.Float(dump_only=True)
    high = ma.Float(dump_only=True)
    low = ma.Float(dump_only=True)
    close = ma.Float(dump_only=True)

class StockInfoSchemaTimesRequested(ma.Schema):
    symbol = ma.String(dump_only=True)
    times_requested = ma.Int(dump_only=True)