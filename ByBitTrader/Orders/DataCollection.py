import datetime

from pybit.unified_trading import HTTP
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import time
import json
import pandas_ta as ta
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import json
import time
from datetime import datetime, timedelta

key = 'YOUR_SECRET'
secret = 'YOUr_API_KEY'

session = HTTP(api_key=key, api_secret=secret, testnet=False)

result = session.get_tickers(
                category="linear").get('result')['list']

tickers = [asset['symbol'] for asset in result if asset['symbol'].endswith('USDT')]
print(tickers)

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


def get_last_timestamp(df):
    return int(df.timestamp[-1:].values[0])


start = int(dt.datetime(2024, 6, 1).timestamp() * 1000)

interval = 60
symbol = 'ETHUSDT'
df = pd.DataFrame()

startTime = datetime.now()
end_time = startTime + timedelta(minutes=2)
while datetime.now() < end_time:
    response = session.get_kline(category='linear',
                                 symbol=symbol,
                                 start=start,
                                 interval=interval).get('result')

    latest = format_data(response)

    if not isinstance(latest, pd.DataFrame):
        break

    start = get_last_timestamp(latest)

    time.sleep(0.2)

    df = pd.concat([df, latest])
    print(f'Collecting data starting {dt.datetime.fromtimestamp(start / 1000)}')
    if len(latest) == 1: break

df.drop_duplicates(subset=['timestamp'], keep='last', inplace=True)

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


def get_last_timestamp(df):
    return int(df.timestamp[-1:].values[0])


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


start = int(dt.datetime(2024, 6, 1).timestamp() * 1000)

interval = 'D'
symbol = 'ETHUSDT'
df = pd.DataFrame()

startTime = datetime.now()
end_time = startTime + timedelta(minutes=2)
while datetime.now() < end_time:
    response = session.get_kline(category='linear',
                                 symbol=symbol,
                                 start=start,
                                 interval=interval).get('result')

    latest = format_data(response)

    if not isinstance(latest, pd.DataFrame):
        break

    start = get_last_timestamp(latest)

    time.sleep(0.2)

    df = pd.concat([df, latest])
    print(f'Collecting data starting {dt.datetime.fromtimestamp(start / 1000)}')

df[['lower_band', 'mid', 'upper_band' ]] = ta.bbands(df.close, length=20, std=2).iloc[:, :3]

print(df[-1:][['lower_band', 'mid','close' , 'upper_band' ]])

df['short_signal'] = np.where(df.close > df.upper_band, 1, 0)
df['long_signal'] = np.where(df.close < df.lower_band, 1, 0)

## lets plot the most recent 100 days
df[['lower_band', 'mid', 'close', 'upper_band']].plot(style=['k--', 'k-', 'b-', 'k--'])

plt.plot(df[df.long_signal==1]['close'], '^g')
plt.plot(df[df.short_signal==1]['close'], 'vr')
plt.title('Bollinger Bands Entries')
plt.ylabel('ETH Price USDT')
plt.show()

start = int(dt.datetime(2024, 6, 1).timestamp())

interval = 240
symbol = 'ETHUSDT'
df = pd.DataFrame()

startTime = datetime.now()
end_time = startTime + timedelta(minutes=5)
while datetime.now() < end_time:

    response = session.get_kline(category='linear',
                                 symbol=symbol,
                                 start=start,
                                 interval=interval).get('result')



    latest = format_data(response)

    if not isinstance(latest, pd.DataFrame):
        break

    start = get_last_timestamp(latest)

    time.sleep(0.2)

    df = pd.concat([df, latest])
    print(f'Collecting data starting {dt.datetime.fromtimestamp(start / 1000)}')

    if len(latest) == 1:
        break

df[['SUPERT', 'direction', 'long', 'short']] = ta.supertrend(df.high,
                                                             df.low,
                                                             df.close,
                                                             length=7,
                                                             multiplier=3)

plt.style.use('ggplot')
df.close.plot(label='close',color='black')
df.long.dropna().plot(label='long', style='go',  markersize=1)
df.short.dropna().plot(label='short', style='ro',  markersize=1)
plt.ylabel('ETHUSDT')
plt.title('Super Trend Indicator')
plt.legend()
plt.show()

df['return'] = df.close.pct_change()
df.dropna(subset=['return'], inplace=True)
df['strategy'] = df.direction * df['return'].shift(-1)
df.dropna(subset=['strategy'], inplace=True)

(df['strategy']+1).cumprod().plot(label='Super Trend')
(df['close']/ df.close[:1].values[0]).plot(label='Buy and Hold')
plt.title('SuperTrend Backtest')
plt.ylabel('Cumulative Returns')
plt.legend()
plt.show()