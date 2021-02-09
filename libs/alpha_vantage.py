import typing

import json
import os

import aiohttp
from aiohttp import web


class AlphaVantage:
    def __init__(self):
        self.apikey = os.getenv("ALPHA_VANTAGE")

    async def get_exchange_rate(self, from_curr: str, to_curr: str) -> dict:
        key = self.apikey
        async with aiohttp.ClientSession() as sess:
            async with sess.get(
                    f"""https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_curr}&to_currency={to_curr}&apikey={key}"""
            ) as resp:
                if resp.status == 404:
                    raise aiohttp.web.HTTPNotFound
                js = json.loads(await resp.text())
                new_dict = {}
                for key, value in js["Realtime Currency Exchange Rate"].items():
                    new_dict[key] = value
                return new_dict
