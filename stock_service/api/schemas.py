# encoding: utf-8

from stock_service.extensions import marsh


class StockSchema(marsh.Schema):

    symbol = marsh.String(dump_only=True)
    name = marsh.String(dump_only=True)
    date = marsh.String(dump_only=True)
    time = marsh.String(dump_only=True)
    open = marsh.String(dump_only=True)
    high = marsh.String(dump_only=True)
    low = marsh.String(dump_only=True)
    close = marsh.String(dump_only=True)
