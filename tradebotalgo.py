from tkinter.tix import Tree
import pandas as pd
import requests
import json
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import time

# api keys 
    # The fmpapi key is "DEMO" this key has been replaced by a demo key 
    # to obtaian your own free key for this model go to https://site.financialmodelingprep.com/developer/docs/ and create an account 


api_key = "DEMO"

class TradeData():

    def startfile():
        localtime = time.ctime(time.time())
        print ("Local current time :", localtime)
        TradeData.simplefile()
        TradeData.checkfile()

    def simplefile():
        # simple code to write a json file so you can load the information into it and if its there then to pass 
        try:
            tryfile= open("StockInfo.json",'x')
            json.dump([],tryfile)
        except:
            pass
    
    def checkfile():
        with open("StockInfo.json",'r') as StockDataR:
            try:
            #   try is used to try to see if something works and if there is an error then it will move on to the except
                StockData = json.load(StockDataR)
                if StockData != []:
                    thislist1=TradeData.simplelist()
                #   if data already populates the json file 
                    TradeData.append_to_file(thislist1)
                
                elif StockData == []:
                    thislist1 = "z"
                # if data is empty then go to writing for the file
                    TradeData.append_to_file(thislist1)
            except:
                thislist1 = "z"
                TradeData.append_to_file(thislist1)
                pass

    def append_json_file(new_data, StockFile="StockInfo.json"):
        #   write data to the end of the json file in an easy and repeatable way
        with open(StockFile,'r+') as Sfile:
            sfile_data = json.load(Sfile)
            sfile_data.append(new_data)
            Sfile.seek(0)
            json.dump(sfile_data,Sfile)
        pass

    def simplelist():
        StockDataR = open("StockInfo.json",'r')
        # open the json storage file
        StockData = json.load(StockDataR)
        #convert json text to python
        thislist1 = []
        # create a list
        for sname in StockData:
            name1 = sname['Symbol']
            thislist1.append(name1)
            #sort through the data in the json file and add it to the list
        return thislist1

    def data_dict(stock_symbol,Sdate,stock_name,stock_year_price,stockDIVs,StockNet,stockEv,StockEps,StockDEps,ss,ssd):
        allstockinfo = {}
        #   create a dict within
        allstockinfo[stock_symbol] = {}
        #   create a nested information within a dict
        allstockinfo[stock_symbol]['Symbol']                = stock_symbol
        allstockinfo[stock_symbol]['Date']                  = Sdate
        allstockinfo[stock_symbol]['Name']                  = stock_name
        allstockinfo[stock_symbol]['StockYearPrice']        = stock_year_price
        allstockinfo[stock_symbol]['StockYearDiv']          = stockDIVs
        allstockinfo[stock_symbol]["NetIncome"]             = StockNet
        allstockinfo[stock_symbol]["EnterpriseValue"]       = stockEv
        allstockinfo[stock_symbol]['Eps']                   = StockEps
        allstockinfo[stock_symbol]['DilutedEps']            = StockDEps
        allstockinfo[stock_symbol]['NumberShares']          = ss
        allstockinfo[stock_symbol]['NumberSharesDiluted']   = ssd
        TradeData.append_json_file(allstockinfo[stock_symbol])

    def f1(string):
        return string.isalpha() 

    # https://financialmodelingprep.com/api/v3/stock/list?apikey={api_key}
    def append_to_file(thislist1):
        # making a global list to check for duplicates from 
        # stock_research = requests.get(f'https://financialmodelingprep.com/api/v3/stock/list?apikey={api_key}')
        try:
            stock_research = requests.get(f'https://financialmodelingprep.com/api/v3/stock/list?apikey={api_key}').json()
            total_stock_list = []
            print(thislist1)
            #   create an initial dictionary for information
            for StockR in stock_research:
                stock_symbol = StockR['symbol']
                stock_name = StockR['name']

                total_stock_list.append(stock_symbol)
                test = stock_symbol.isalpha()
                if stock_symbol not in thislist1:
                    if  TradeData.f1(stock_symbol) == True:
                        # check to see if a stock is already in the list or not if it is then pass and if it isnt then run program to add it to the json file 
                        stock_IS = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{stock_symbol}?limit=5&apikey={api_key}").json()
                        if not stock_IS:
                            pass
                        else:
                            Sdate           = stock_IS[0]["date"]
                            StockNet        = stock_IS[0]["netIncome"]
                            StockEps        = stock_IS[0]["eps"]
                            StockDEps       = stock_IS[0]["epsdiluted"]
                            ss              = stock_IS[0]["weightedAverageShsOut"]
                            ssd             = stock_IS[0]["weightedAverageShsOutDil"]
                            if StockNet > 0:
                                stock_EV = requests.get(f"https://financialmodelingprep.com/api/v3/enterprise-values/{stock_symbol}?limit=5&apikey={api_key}").json()
                                if not stock_EV:
                                    pass
                                else:
                                    stock_year_price = stock_EV[0]["stockPrice"]
                                    stockEv = stock_EV[0]["enterpriseValue"]
                                    stockmarketcap = stock_EV[0]["marketCapitalization"]
                                    if stockEv > 0:
                                        stock_Div = requests.get(f"https://financialmodelingprep.com/api/v3/profile/{stock_symbol}?apikey={api_key}").json()
                                        if not stock_Div:
                                            pass
                                        else:
                                            sdiv1  = stock_Div[0]["lastDiv"]
                                            stockDIVs = sdiv1*4
                                            if stockDIVs>0:

                                                TradeData.data_dict(stock_symbol,Sdate,stock_name,stock_year_price,stockDIVs,StockNet,stockEv,StockEps,StockDEps,ss,ssd)
                                                #   print(stock_symbol,stock_name,stock_price,'\n',stock_industry,stock_sector,stock_country,'\n',StockValue,StockDebt,SVal,'\n',SVal1)
                                                #   with plan 0.2 * number of calls
                                                # 0.2* 4 =0.8 = rounded to 1sec
                                                # 1 for testing with a data plan and 1728 for full work with a demo plan
                                                time.sleep(1728)
                                                #print(stock_symbol)
                                                print("(Added )Length of stock symbols",len(total_stock_list),stock_symbol)
                                            else:
                                                pass
                                    else:
                                        pass
                            else:
                                pass
                    else:
                        pass
            
                print("(Pass)Length of stock symbols",stock_symbol,len(total_stock_list))
                #with plan 0.2 * number of calls
                # 0.2* 4 =0.8 = 1sec
                # 0.2* 4 =0.8 = rounded to 1sec
                # 1 for testing with a data plan and 1728 for full work with a demo plan
                time.sleep(1728)
                #
            else:
                pass

                # if thislist1 >= 39145:
                #     print("complete")
                #     break
        except:
            print('connetion failed Append')
            pass

while True:
    TradeData.startfile()

