import time
from pybit.unified_trading import WebSocket
from collections import deque
import json

#with open('authcreds.json') as j:
#    creds = json.load(j)

key = 'YOUR_SECRET'
secret = 'YOUr_API_KEY'

public = WebSocket(channel_type='linear', testnet=False)
private = WebSocket(channel_type='private',
                    api_key=key,
                    api_secret=secret,
                    testnet=False)

################   Stream Live Orderbook Data   ################################################

# stream level one orderbook data i.e. the best bid, ask with corresponding volumes for each level.
# This function extracts the relevant data and appends it to a list we have defined called orderbook.
# We have also created a loop for illustrative purposes to show a) how fast this list will grow b) how a user can
# extract the latest data from this list. A trader may want to have functionality like this to optimally place orders
# at the touch.


'''
orderbook = []

def handle_orderbook_message(message):
    
    #custom on callback function for orderbook stream , insert given values
    #in to dictionary to be appended to oderbook list.
    #None.

    data = message.get('data', None)

    global orderbook

    current = {}
    if data:
        try:
            current['asset'] = data.get('s')
            current['best_bid'] = float(data.get('b')[0][0])
            current['bid_volume'] = float(data.get('b')[0][1])
            current['best_ask'] = float(data.get('a')[0][0])
            current['ask_volume'] = float(data.get('a')[0][1])
            orderbook.append(current)
        except (TypeError, IndexError, AttributeError):
            pass


public.orderbook_stream(depth=1, symbol='ETHUSDT', callback=handle_orderbook_message)

import time

for _ in range(10):
    print(len(orderbook))
    time.sleep(1)
    print(orderbook[-1])

# In addition the trader may want to store this orderbook data to a database once it reaches a certain length.
# A useful trick for this is to use a deque object as shown below.

orderbook = deque(maxlen=(1000))

# The logic above ensures, that a maximum of 1000 datapoints will be stored in the list.

'''

###########################    Stream Live Trades    ####################################

# Lets say we wanted to stream live trades for ETHUSDT contract and save large trades.
# we will write a callback function that prints to the console when there is a trade over $50,000
# Traders may be interested in large order sizes as this can be indicative of which direction whales are trading in.
'''

THRESHOLD = 50_000


def handle_trade_message(message):
    
        #message example
        #{
        #"topic": "publicTrade.ETHUSDT",
        #"type": "snapshot",
        #"ts": 1672304486868,
        #"data": [
         #   {
         #       "T": 1672304486865,
         #       "s": "ETHUSDT",
         #       "S": "Buy",
         #       "v": "0.001",
         #       "p": "16578.50",
         #       "L": "PlusTick",
         #       "i": "20f43950-d8dd-5b31-9112-a178eb6023af",
         #       "BT": false
         #           }
         #       ]
         #   }


        #custom callback to detect trades over a certain size



    try:
        data = message.get('data')
        for trade in data:
            value = float(trade.get('v')) * float((trade.get('p')))

            if value > THRESHOLD:
                print(f"A trade to {trade.get('S')} {value} was just executed")
            else:
                pass
    except (ValueError, AttributeError):
        pass


public.trade_stream(symbol='ETHUSDT', callback=handle_trade_message)

'''

##############   Replicate Coinglass Liquidation Data   ###############################

# A crypto liquidation occurs when a trader's position in a cryptocurrency or other digital asset is forcibly closed
# by the exchange or platform on which the trade was made.
# This happens when the value of the trader's position falls below a certain threshold known as the liquidation price.
# When this occurs, the exchange or platform will automatically sell off the trader's position in order to protect
# itself and other traders from further losses.
# Below we make a script that calculates the hourly long/short liquidations for ETHUSDT. We print out the running total
# every 30 seconds also.
'''

long_liqs = []
short_liqs = []


def handle_liquidation_message(message):
    
    #{
    #"data": {
    #    "price": "0.03803",
    #    "side": "Buy",
    #    "size": "1637",
    #    "symbol": "ETHUSDT",
    #    "updatedTime": 1673251091822
    #},
    #"topic": "liquidation.GALAUSDT",
    #"ts": 1673251091822,
    #"type": "snapshot"
    #}

    global long_liqs, short_liqs

    try:
        data = message.get('data')
        if data.get('side') == 'Buy':
            usd_val = float(data.get('size')) * float(data.get('price'))
            print(f'A long degen just got liquidated for {usd_val}')
            long_liqs.append(usd_val)
        elif data.get('side') == 'Sell':
            usd_val = float(data.get('size')) * float(data.get('price'))
            print(f'A short degen just got liquidated for {usd_val}')
            short_liqs.append(usd_val)
        else:
            pass
    except (TypeError, ValueError, IndexError):
        pass


public.liquidation_stream(symbol='ETHUSDT', callback=handle_liquidation_message)

import datetime as dt

while True:

    timenow = dt.datetime.now()

    if timenow.minute == 0 and timenow.second == 0:
        print(f'A total of {sum(long_liqs)} longs have been rekt in last hour')
        print(f'A total of {sum(short_liqs)} shorts have been rekt in last hour')
        # reset the lists for the next hour of slaughter
        longs_liqs = []
        short_liqs = []
        time.sleep(1)

    elif timenow.second % 30 == 0:
        print(f'A total of {sum(long_liqs)} longs have been rekt so far in this hour')
        print(f'A total of {sum(short_liqs)} shorts have been rekt so far in this hour')
        time.sleep(1)

'''

############################    Streaming Position   #############################################################
# Below we create a position stream to keep track of how much ETH we currently have. We also do our bit to help the
# ETH community.

'''

eth_position = 0


def handle_position_message(message):

    #custom error message to retrieve position of given asset.

    global eth_position
    try:
        data = message.get('data', [])
        for pos in data:
            if pos['symbol'] == 'ETHEUSDT':
                if pos['side'] == 'Sell':
                    eth_position = - float(pos['size'])
                elif pos['side'] == 'Buy':
                    eth_position = float(pos['size'])
                else:
                    eth_position = 0
            else:
                pass
    except (IndexError, AttributeError, TypeError):
        pass


private.position_stream(callback=handle_position_message)

while True:

    if eth_position > 0:
        print(f'Excellent you just bought  {eth_position} ETH!!!!!!!')
        break
    elif eth_position < 0:
        print(f'Not breaking until you buy a ETH bagholders must resort to extraordinary measures while underwater')
    else:
        print('Waiting for you to buy a ETH ')

'''

#######################   Stream Orders   ##########################################################

# Lets say we are creating an order management system, to monitor fills on an algorithm, well, we need to keep a track
# of order states. Below are the different states an order can take.
# Created: order has been accepted by the system but not yet put through the matching engine
# New: order has been placed successfully
# Rejected
# PartiallyFilled
# PartiallyFilledCanceled: Only spot has this order status
# Filled
# Cancelled: In derivatives, orders with this status may have an executed qty
# Untriggered
# Triggered
# Deactivated
# Active: order has been triggered and the new active order has been successfully placed. Is the final state of a successful conditional orde


# Since creating an order management system is quite complex we simply print the results of orders from the API below:

def handle_orders_message(message):
    print(message)


private.order_stream(callback=handle_orders_message)
