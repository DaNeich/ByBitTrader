from pybit.unified_trading import HTTP
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import time
import json
import BybitConnector

# Endpoints
api_url = "https://api.bybit.com"
derivatives = "/derivatives/v3/public/order-book/L2"
mergedOrderBook = "/spot/v3/public/quote/depth/merged"
bestBidAskPrice = "/spot/v3/public/quote/ticker/bookTicker"
symbol = "ETHUSDT"

session = BybitConnector.newSession()

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

########## Trigger Orders #########################################
# Lets say a trader believes that if DOGE will break through $0.10 (when price currently $0.07) it will reach $0.15 ,
# well , he could place a trigger order to market buy 1 DOGE at $0.10 and another one to sell 1 DOGE if the price
# crosses above $0.15. The function calls below achieve this logic. These orders are known as conditional i.e. if the
# condition (trigger price) isn't met they won't be executed.

# trigger to buy DOGE if the price crosses above $0.1
response = session.place_order(
    category='linear',
    symbol = 'DOGEUSDT',
    orderType = 'Market',
    triggerDirection = 1,
    side= 'Buy',
    qty= '1',
    triggerPrice='0.1'
    )

#Lets say a trader believes that in the event of DOGE falling below $0.049 , this will mean that $0.05 will become
# resistance. Well, he could place a conditional limit order that if the price should fall below 0.049 this will send a
# limit order to 0.05.

# trigger to sell DOGE if the price crosses above $0.15
response = session.place_order(
    category='linear',
    symbol = 'DOGEUSDT',
    orderType = 'Market',
    triggerDirection = 1,
    side= 'Sell',
    qty= '1',
    triggerPrice='0.15'
    )

 ################# GET INFO ETHUSDT CONTRACT TO AVOID NUMBER ERRORS WHILE PLACING ORDERS ###############################
info = session.get_instruments_info(category='linear')

symbols = info.get('result').get('list')


def get_symbol_info(symbol, symbols):
    info = [x for x in symbols if x['symbol'] == symbol]
    if info:
        return info[0]

    raise Exception(f'Information for symbol = {symbol} not found')


print(get_symbol_info('ETHUSDT', symbols))
