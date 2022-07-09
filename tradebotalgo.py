import pandas as pd
import requests
import json
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import time

# create a True phrase or a phrase that enables and disables a while loop
do = True

# The api key is "494a1352ffaaa042a40101d33af58da0"
api_key = '494a1352ffaaa042a40101d33af58da0'
def simplefile():
    # simple code to write a json file so you can load the information into it and if its there then to pass 
    try:
        tryfile= open('StockDataInfo.json','x')
        json.dump([],tryfile)
    except:
        pass
    
def checkfile():
    with open('StockDataInfo.json','r') as StockDataR:
        try:
        #   try is used to try to see if something works and if there is an error then it will move on to the except
            StockData = json.load(StockDataR)
            if StockData != []:
            #   if data already populates the json file 
                
                append_to_file()
                stock_research = requests.get(f'https://financialmodelingprep.com/api/v3/available-traded/list?apikey={api_key}')
                stock_research = stock_research.json()
            
                #print lengths to make sure all data is aquired
                listname1 = []
                for f in stock_research:
                     stock_symbol = f['symbol']
                     stock_name = f['name']
                     listname1.append(stock_symbol)
                print(len(listname1))

                listname2 = []
                for i in StockData:
                    name = i['symbol']
                    listname2.append(name)
                print(len(listname2))

                #if len(listname1) == len(listname2):
                    #if the two data sets are the same length then all the data is aquired
                data_print()
                return False

            elif StockData == []:
            # if data is empty then go to writing for the file
                write_to_file()
        except:
            write_to_file()
            pass

def append_json_file(new_data, StockFile="StockDataInfo.json"):
    #   write data to the end of the json file in an easy and repeatable way
    with open(StockFile,'r+') as Sfile:
        sfile_data = json.load(Sfile)
        sfile_data.append(new_data)
        Sfile.seek(0)
        json.dump(sfile_data,Sfile)
    pass

# https://financialmodelingprep.com/api/v3/stock/list?apikey=494a1352ffaaa042a40101d33af58da0
def write_to_file():

    try:
    #stock_research = requests.get(f'https://financialmodelingprep.com/api/v3/stock/list?apikey={api_key}')
        stock_research = requests.get(f'https://financialmodelingprep.com/api/v3/available-traded/list?apikey={api_key}')
        stock_research = stock_research.json()
    
        allstockinfo = {}
        #   create an initial dictionary for information
        for StockR in stock_research:
            stock_symbol = StockR['symbol']
            stock_name = StockR['name']
            stock_price = StockR['price']
            
            StockP = requests.get(f'https://financialmodelingprep.com/api/v3/profile/{stock_symbol}?apikey={api_key}').json()
            if not StockP:
                stock_industry = 'unknown'
                stock_sector   = 'unknown'
                stock_country  = 'unknown'
            else:
                stock_industry = StockP[0]['industry']
                stock_sector   = StockP[0]['sector']
                stock_country  = StockP[0]['country']
            
            StockV = requests.get(f'https://financialmodelingprep.com/api/v3/enterprise-values/{stock_symbol}?limit=40&apikey={api_key}').json()
            if not StockV:
                StockNumShare = "uknown"
                StockValue    = "uknown"
                StockDebt     = "uknown"
                SVal          = "uknown"
                SVal1         = "uknown"
            else:
                StockNumShare = StockV[0]['numberOfShares']
                StockValue = StockV[0]['minusCashAndCashEquivalents']
                StockDebt = StockV[0]['addTotalDebt']
                SVal = StockValue - StockDebt
                if SVal <= 0:
                    SVal1 = 'Incase of a call to repay All Debts The company Will close and foreclose'
                elif SVal >= 0:
                    SVal1= 'Incase of a call to repay All Debts The company will Not close and foreclose'

            StockI = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{stock_symbol}?limit=120&apikey={api_key}').json()
            if not StockI:
                StockRev = 0
                StockCostRev = 0
                StockNet = 0
                Sdate         = "uknown"
            else:
                StockRev = StockI[0]['revenue']
                StockCostRev = StockI[0]['costOfRevenue']
                StockNet = StockI[0]['netIncome']
                Sdate         = StockI[0]["date"]

            #   create a dict within
            allstockinfo[stock_symbol] = {} 
            #   create a nested information within a dict
            allstockinfo[stock_symbol]['symbol']        = stock_symbol
            allstockinfo[stock_symbol]['name']          = stock_name
            allstockinfo[stock_symbol]['industry']      = stock_industry
            allstockinfo[stock_symbol]['sector']        = stock_sector
            allstockinfo[stock_symbol]['country']       = stock_country
            allstockinfo[stock_symbol]['date']          = Sdate
            allstockinfo[stock_symbol]['cash']          = StockValue
            allstockinfo[stock_symbol]['debt']          = StockDebt
            allstockinfo[stock_symbol]['valuation']     = SVal
            allstockinfo[stock_symbol]['totalrevenue']  = StockRev
            allstockinfo[stock_symbol]['netincome']     = StockNet

            #print(stock_symbol,stock_name,stock_price,'\n',stock_industry,stock_sector,stock_country,'\n',StockValue,StockDebt,SVal,'\n',SVal1)
            #with plan 0.2 * number of calls
            # 0.2* 4 =0.8 = rounded to 1sec
            # 1 for testing with a data plan and 1728 for full work with a demo plan
            time.sleep(1)
            #print(stock_symbol)
            append_json_file(allstockinfo[stock_symbol])
    except:
        pass

    #stockdata = pd.DataFrame.from_dict(allstockinfo)
    #print(stockdata)



# https://financialmodelingprep.com/api/v3/stock/list?apikey=494a1352ffaaa042a40101d33af58da0
def append_to_file():
   #stock_research = requests.get(f'https://financialmodelingprep.com/api/v3/stock/list?apikey={api_key}')
    try:
        stock_research = requests.get(f'https://financialmodelingprep.com/api/v3/available-traded/list?apikey={api_key}')
        stock_research = stock_research.json()

        
        StockDataR = open('StockDataInfo.json','r')
        # open the json storage file
        StockData = json.load(StockDataR)
        #convert json text to python
        thislist1 = []
        # create a list
        for sname in StockData:
            name1 = sname['name']
            thislist1.append(name1)
            #sort through the data in the json file and add it to the list

        total_stock_list = []

        allstockinfo = {}
        #   create an initial dictionary for information
        for StockR in stock_research:
            stock_symbol = StockR['symbol']
            stock_name = StockR['name']
            stock_price = StockR['price']

            total_stock_list.append(stock_symbol)

            if stock_name not in thislist1:
                # check to see if a stock is already in the list or not if it is then pass and if it isnt then run program to add it to the json file 
            
                StockP = requests.get(f'https://financialmodelingprep.com/api/v3/profile/{stock_symbol}?apikey={api_key}').json()
                if not StockP:
                    stock_industry = 'unknown'
                    stock_sector   = 'unknown'
                    stock_country  = 'unknown'
                else:
                    stock_industry = StockP[0]['industry']
                    stock_sector   = StockP[0]['sector']
                    stock_country  = StockP[0]['country']
                
                StockV = requests.get(f'https://financialmodelingprep.com/api/v3/enterprise-values/{stock_symbol}?limit=40&apikey={api_key}').json()
                if not StockV:
                    StockNumShare = 0
                    StockValue    = 0
                    StockDebt     = 0
                    SVal          = 0
                    SVal1         = 0
                else:
                    StockNumShare = StockV[0]['numberOfShares']
                    StockValue = StockV[0]['minusCashAndCashEquivalents']
                    StockDebt = StockV[0]['addTotalDebt']
                    SVal = StockValue - StockDebt
                    if SVal <= 0:
                        SVal1 = 'Incase of a call to repay All Debts The company Will close and foreclose'
                    elif SVal >= 0:
                        SVal1= 'Incase of a call to repay All Debts The company will Not close and foreclose'

                StockI = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{stock_symbol}?limit=120&apikey={api_key}').json()
                if not StockI:
                    StockRev = 0
                    StockCostRev = 0
                    StockNet = 0
                    Sdate         = "uknown"
                else:
                    StockRev = StockI[0]['revenue']
                    StockCostRev = StockI[0]['costOfRevenue']
                    StockNet = StockI[0]['netIncome']
                    Sdate         = StockI[0]["date"]

                #   create a dict within
                allstockinfo[stock_symbol] = {}
                #   create a nested information within a dict
                allstockinfo[stock_symbol]['symbol'] = stock_symbol 
                allstockinfo[stock_symbol]['name'] = stock_name
                allstockinfo[stock_symbol]['industry'] = stock_industry
                allstockinfo[stock_symbol]['sector'] = stock_sector
                allstockinfo[stock_symbol]['country'] = stock_country
                allstockinfo[stock_symbol]['date'] = Sdate
                allstockinfo[stock_symbol]['cash'] = StockValue
                allstockinfo[stock_symbol]['debt'] = StockDebt
                allstockinfo[stock_symbol]['valuation'] = SVal
                allstockinfo[stock_symbol]['netincome'] = StockNet

                #print(stock_symbol,stock_name,stock_price,'\n',stock_industry,stock_sector,stock_country,'\n',StockValue,StockDebt,SVal,'\n',SVal1)
                
                #with plan 0.2 * number of calls
                # 0.2* 4 =0.8 = rounded to 1sec
                # 1 for testing with a data plan and 1728 for full work with a demo plan
                time.sleep(1)
                #print(stock_symbol)
                print("Length of stock symbols",len(total_stock_list))
                append_json_file(allstockinfo[stock_symbol])
    except:
        print('connetion failed')
        pass


def data_print():
    StockDataR = open('StockDataInfo.json','r')
    StockData = json.load(StockDataR)
    PD_Stock_Data = pd.DataFrame.from_dict(StockData)
    #print(PD_Stock_Data)

    df = PD_Stock_Data
 
    # plotting the bubble chart
    size = ((PD_Stock_Data['netincome']**2)//2)
    fig = px.scatter(df, x="sector", y="valuation",
                    size=size, color="country")
    
    # showing the plot
    fig.show()

    df1 = PD_Stock_Data
    
    # plotting the bubble chart
    size = ((PD_Stock_Data['netincome']**2)//2)
    fig1 = px.scatter(df1, x="country", y="valuation",
                    size=size, color="sector")
    
    # showing the plot
    fig1.show()
    #return False


while do == True:
    localtime = time.ctime(time.time())
    print ("Local current time :", localtime)
    simplefile()
    #checkfile()
    do = checkfile()
    #data_print()
    #break
        
