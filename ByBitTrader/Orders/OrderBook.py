from pybit.unified_trading import HTTP
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import time
import json
import BybitConnector

session = BybitConnector.newSession()


# Get List of  Available USDT Perpetuals Bybit
########### TICKERS ###########################
# uniquely identify a particular cryptocurrency. For example, Bitcoin's ticker is "BTC", Ethereum's ticker is "ETH", and so on
# ickers are used to track the performance of a particular cryptocurrency and to provide easy reference when discussing or trading that cryptocurrency.
'''
result = session.get_tickers(
                category="linear").get('result')['list']

tickers = [asset['symbol'] for asset in result if asset['symbol'].endswith('USDT')]
print(tickers)

'''

# Get Historical Daily Data
response = session.get_kline(category='linear',
                             symbol='ETHUSDT',
                             interval='D').get('result')


def format_data(response):
    '''


    Parameters
    ----------
    respone : dict
        response from calling get_klines() method from pybit.

    Returns
    -------
    dataframe of ohlc data with date as index

    '''
    data = response.get('list', None)

    if not data:
        return

    data = pd.DataFrame(data,
                        columns=[
                            'timestamp',
                            'open',
                            'high',
                            'low',
                            'close',
                            'volume',
                            'turnover'
                        ],
                        )

    f = lambda x: dt.datetime.utcfromtimestamp(int(x) / 1000)
    data.index = data.timestamp.apply(f)
    return data[::-1].apply(pd.to_numeric)


df = format_data(response)

print(df)

# The problem with this approach is that we are constrained to only 200 rows of data. Therefore if we want data exceeding (in this case) 200 days we have to
# make multiple function calls. Let's say we wanted to get hourly data for ETH since the start of 2023. We will have to make multiple API calls.
def get_last_timestamp(df):
    return int(df.timestamp[-1:].values[0])


start = int(dt.datetime(2024, 6, 28).timestamp() * 1000)

interval = 60
symbol = 'ETHUSDT'
df = pd.DataFrame()

while True:
    response = session.get_kline(category='linear',
                                 symbol=symbol,
                                 start=start,
                                 interval=interval).get('result')

    latest = format_data(response)

    if not isinstance(latest, pd.DataFrame):
        break

    start = get_last_timestamp(latest)

    time.sleep(0.1)

    df = pd.concat([df, latest])
    print(f'Collecting data starting {dt.datetime.fromtimestamp(start / 1000)}')
    if len(latest) == 1: break

df.drop_duplicates(subset=['timestamp'], keep='last', inplace=True)


############################## GET ORDER BOOK ################################

print("Getting Orderbook")

response = session.get_orderbook(
    category="linear",
    symbol="ETHUSDT",
    limit=50).get('result')


def format_order_book(response):
    '''


    Parameters
    ----------
    response : dict

    Returns
    -------
    two list of lists containing bid/ask price with associated volume

    '''
    bids = response.get('b')
    asks = response.get('a')

    return bids, asks


bids, asks = format_order_book(response)

for bid in bids[:10]:
    print(f'Bid price - {bid[0]} , quantity = {bid[1]}')


#############################     Get Open Interest Data    ###########################################################
# Open interest is an important indicator of market liquidity and sentiment, as it represents the number of market
# participants who are actively trading a particular futures contract.


#Parameter	Required	Type	Comments
#category	true	string	Product type. linear,inverse
#symbol	true	string	Symbol name
#intervalTime	true	string	Interval. 5min,15min,30min,1h,4h,1d
#startTime	false	integer	The start timestamp (ms)
#endTime	false	integer	The end timestamp (ms)
#limit	false	integer	Limit for data size

def format_oi(response):
    '''


    Parameters
    ----------
    respone : dict
        response from calling get_open_interest

    Returns
    -------
    dataframe of open interest and timestamp

    '''
    data = response.get('list', None)

    if not data:
        return

    ois = []
    tss = []
    for row in data:
        oi = float(row.get('openInterest'))
        ts = int(row.get('timestamp'))
        ois.append(oi)
        tss.append(ts)

    data = pd.DataFrame()
    data['open_interest'] = ois
    data['timestamp'] = tss

    f = lambda x: dt.datetime.utcfromtimestamp(int(x) / 1000)
    data.index = data.timestamp.apply(f)
    return data[::-1]


response = session.get_open_interest(
    category="linear",
    symbol="ETHUSDT",
    intervalTime="1h",
    limit=200
).get('result')

oi = format_oi(response)

