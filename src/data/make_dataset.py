from datetime import date
from dateutil.relativedelta import relativedelta

import pandas as pd

import yfinance as yf
import nasdaqdatalink
import requests

import os

#time range for all queries
start_date = (date.today() - relativedelta(years = 5)).strftime('%Y-%m-%d')
#start date for NBP data limited by NBP API
nbp_start_date = (date.today() - relativedelta(years = 1)).strftime('%Y-%m-%d')
end_date = date.today().strftime('%Y-%m-%d')

#get the gold and silver price USD/oz from Yahoo Finance API
yf_df = yf.download(['GC=F', 'SI=F'],
                          start = start_date,
                          end = end_date,
                          progress = False)
#edit the columns names
#flatten the multi-level columns
yf_df.columns = yf_df.columns.map('_'.join).str.replace('GC=F', 'Gold').str.replace('SI=F', 'Silver')

#gold/sliver ratio based on the adjusted close prices
yf_df['Gold/Silver_Ratio'] = yf_df['Adj Close_Gold']/yf_df['Adj Close_Silver']

#get USD/PLN exchange rate from NBP (Polish National Bank) API
def nbp_exchange_rates_func(currency_code):
    url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency_code}/{nbp_start_date}/{end_date}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    elif response.status_code == 404:
        print(f'Error: Failed to fetch data. Status code: {response.status_code} Not Found')
        return None
    elif response.status_code == 400:
        print(f'Error: Failed to fetch data. Status code: {response.status_code} Bad Request')
        return None
    
currency_code = 'USD'
nbp_exchange_rates = nbp_exchange_rates_func(currency_code)

#convert json data format to DataFrame
if nbp_exchange_rates:
    nbp_exchange_rates = pd.DataFrame(nbp_exchange_rates['rates'])
        
#edit the columns names
new_columns_names = {
    'no' : 'Table Number',
    'effectiveDate' : 'Date',
    'mid' : 'Average Exchange Rate of ' + str(currency_code) #applicable only for A Table
    #'bid' : 'Buying Rate', #applicable only for C Table
    #'ask' : 'Selling Rate' #applicable only for C Table
}

nbp_exchange_rates = nbp_exchange_rates.rename (columns = new_columns_names)

#convert 'Date' column to index
nbp_exchange_rates = nbp_exchange_rates.set_index('Date')

#get the recalculated gold price from NBP (Polish National Bank) API
#price of 1oz gold (of 1000 millesimal fineness) calculated at NBP
def nbp_gold_price_func():
    url = f"https://api.nbp.pl/api/cenyzlota/{nbp_start_date}/{end_date}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    elif response.status_code == 404:
        print(f'Error: Failed to fetch data. Status code: {response.status_code} Not Found')
        return None
    elif response.status_code == 400:
        print(f'Error: Failed to fetch data. Status code: {response.status_code} Bad Request')
        return None

nbp_gold_price = nbp_gold_price_func()

#convert json data format to DataFrame
if nbp_gold_price:
    nbp_gold_price = pd.DataFrame(nbp_gold_price)
        
#edit the columns names
new_columns_names = {
    'data' : 'Date',
    'cena' : 'NBP Gold Price'
}

nbp_gold_price = nbp_gold_price.rename (columns = new_columns_names)

#convert 'Date' column to index
nbp_gold_price = nbp_gold_price.set_index('Date')
#convert gram price to ounce price
#Banker's rounding used (round half to even)
oz_g = 31.1034768
nbp_gold_price['NBP Gold Price [PLN/oz]'] = round(nbp_gold_price['NBP Gold Price'] * oz_g, 4)

#get the gold and silver price USD/oz from LBMA
nasdaqdatalink.ApiConfig.api_key = os.environ.get('NASDAQ_API_KEY')
lbma_df = nasdaqdatalink.get(['LBMA/GOLD', 'LBMA/SILVER'], start_date = start_date, end_date = end_date)