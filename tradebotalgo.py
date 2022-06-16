from msilib.schema import Class
import requests
import pandas as pd
import numpy as np
import time

def codetime():
    # The fmpapi key is "DEMO"(will not work without a key) you need to go here https://site.financialmodelingprep.com/developer 
    # and make an free account to get your free api key
    fmp_api_key = 'demo'
    #stock_research = requests.get(f'https://financialmodelingprep.com/api/v3/stock/list?apikey={api_key}')
    fmp_stock_research = requests.get(f'https://financialmodelingprep.com/api/v3/available-traded/list?apikey={fmp_api_key}')
    fmp_stock_research = fmp_stock_research.json()
    fmp_stock_symbol = []
    for StockR in fmp_stock_research:
        stock_symbol = StockR['symbol']
        fmp_stock_symbol.append(f"{stock_symbol}")
    print(len(fmp_stock_symbol))

class TradeBot():
    def __init__(self,stock):
        self.stock = stock
        pass

