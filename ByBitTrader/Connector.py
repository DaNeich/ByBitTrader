from pybit.unified_trading import HTTP
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import time
import json

#with open('authcreds.json') as j:
#    creds = json.load(j)

key = 'YOUR_SECRET'
secret = 'YOUr_API_KEY'

session = HTTP(api_key=key, api_secret=secret, testnet=False)
from pybit.unified_trading import HTTP

api_url = "https://api.bybit.com"
endpoint = "/derivatives/v3/public/order-book/L2"
mergedOrderBook = "/spot/v3/public/quote/depth/merged"
bestBidAskPrice = "/spot/v3/public/quote/ticker/bookTicker"
symbol = "ETHUSDT"

##############   Authentication   ###############################

#session = HTTP(
#    testnet=False,
#    api_key="8VbxihLMLH9zHJsfRr",
#    api_secret="jBvPJYh5XaKSWQWIfnyZ71s39QwpayEyebrd",


##################################################################



# uniquely identify a particular cryptocurrency. For example, Bitcoin's ticker is "BTC", Ethereum's ticker is "ETH", and so on
# ickers are used to track the performance of a particular cryptocurrency and to provide easy reference when discussing or trading that cryptocurrency.
'''
result = session.get_tickers(
                category="linear").get('result')['list']

tickers = [asset['symbol'] for asset in result if asset['symbol'].endswith('USDT')]
print(tickers)

'''
##################################################################################

response = session.get_kline(category='linear',
                             symbol='ETHUSDT',
                             interval='D').get('result')


#The python script below calls the get_kline method from Pybit. Note that we do not pass the start/end timestamp argument
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


start = int(dt.datetime(2023, 1, 1).timestamp() * 1000)

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


##############################    GET ORDERS BOOK     ##################################################

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

for bid in bids:
    print(f'Bid price - {bid[0]} , quantity = {bid[1]}')


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


###################################################   PLACE ORDER    ##################################################

''''
response = session.place_order(
    category='linear',
    symbol = 'ETHUSDT',
    orderType = 'Market',
    side = 'Buy',
    qty= '0.00000000001'
    )
'''


#############################    Limit Orders    ######################################################################
#############################    PLACE ORDER - Target Price and Stop Loss #############################################

'''
# we can also add a target price and a stop price
response = session.place_order(
    category='linear',
    symbol = 'ETHUSDT',
    orderType = 'Market',
    side = 'Buy',
    qty= '1',
    takeProfit='0.1',
    stopLoss = '0.05'
    )
'''

######################     Different types of orders      ##############################################################

# Good Till Cancel (GTC):
# If we specify GTC as the time in force parameter, the order will rest in the book, until either it is filled or
# canceled by the user.

#GTC order
response = session.place_order(
    category='linear',
    symbol = 'DOGEUSDT',
    orderType = 'Limit',
    timeInForce='GTC',
    side = 'Buy',
    qty= '1',
    price = '0.07849'
    )

# Immediate or Cancel (IOC)
# An IOC order allows traders to execute an order at the best available price in the market, and any part of the order
# that cannot be filled immediately is automatically canceled.

#IOC order
response = session.place_order(
    category='linear',
    symbol = 'DOGEUSDT',
    orderType = 'Limit',
    timeInForce='IOC',
    side = 'Buy',
    qty= '1',
    price = '0.07849'
    )


# Fill or Kill (FOK)
# A FOK order is a type of order which the user can specify that if the order can't be filled in its entirety ,
# it should be canceled e.g. we put a limit order for 100 DOGE at $0.071 , however, there are only 80 DOGE resting in
# the book at the time the order is submitted. This would result in the entire order being canceled and the trader's
# position being unchanged.

#FOK order
response = session.place_order(
    category='linear',
    symbol = 'DOGEUSDT',
    orderType = 'Limit',
    timeInForce='FOK',
    side = 'Buy',
    qty= '1',
    price = '0.08'
    )


# Post Only
# A post only is where a trader places an order on the order book, and if the order would immediately execute against
# an existing order, the order will be canceled instead of being filled. In other words, a Post-Only order ensures that
# your order is added to the order book as a maker order (an order that provides liquidity to the market), rather than
# as a taker order (an order that takes liquidity from the market).

#PostOnly
response = session.place_order(
    category='linear',
    symbol = 'DOGEUSDT',
    orderType = 'Limit',
    timeInForce='PostOnly',
    side = 'Buy',
    qty= '1',
    price = '0.08'
    )

