import datetime
from pybit.unified_trading import HTTP
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta
from scipy.stats import linregress
import datetime as dt

key = 'YOUR_SECRET'
secret = 'YOUr_API_KEY'

session = HTTP(api_key=key, api_secret=secret, testnet=False)


def format_data(response):
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


def get_last_timestamp(df):
    return int(df.timestamp[-1:].values[0])


def get_all_data(sym, interval):
    start = int(dt.datetime(2020, 1, 1).timestamp() * 1000)
    df = pd.DataFrame()
    while True:
        response = session.get_kline(category='linear',
                                     symbol=sym,
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

    return df


interval = 'D'
symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'ADAUSDT', 'DOGEUSDT', 'MATICUSDT', 'SOLUSDT', 'DOTUSDT',
           'LTCUSDT']

dfs = []

for symbol in symbols:
    data = get_all_data(symbol, interval)
    dfs.append(data)

# Merge dataframes, renaming columns to avoid duplicate names
df = pd.DataFrame(data=dfs[0]['close'].rename(symbols[0]))

for i, data in enumerate(dfs[1:], start=1):
    df = pd.merge(df, pd.DataFrame(data['close'].rename(symbols[i])), left_index=True, right_index=True)

# Drop duplicate index entries
df = df[~df.index.duplicated(keep='last')]

# Calculate returns and beta
returns = df.pct_change().dropna()
result = linregress(returns['BTCUSDT'].values, returns['ETHUSDT'].values)
print(f'Beta for ETH regressed on BTC is {result.slope}')

# Strategy calculations
beta_calc = df[df.index < dt.datetime(2022, 9, 1)].pct_change().dropna()
result = linregress(beta_calc['BTCUSDT'].values, beta_calc['ETHUSDT'].values)
beta = result.slope
print(f'Beta for ETH regressed on BTC is {result.slope}')

eth_short = 10_000
btc_long = eth_short * beta
print(f'Longing {btc_long} worth of BTC')

strat = df[(df.index >= dt.datetime(2022, 9, 1)) & (df.index < dt.datetime(2022, 10, 1))][['BTCUSDT', 'ETHUSDT']].pct_change().dropna()
strat['eth_strat_returns'] = (strat['ETHUSDT'] + 1).cumprod()
strat['btc_strat_returns'] = (strat['BTCUSDT'] + 1).cumprod()
strat['combined_returns'] = (strat['ETHUSDT'] * -1 + strat['BTCUSDT'] * beta)
strat['strategy_returns'] = (strat['combined_returns'] + 1).cumprod()
strat[['eth_strat_returns', 'btc_strat_returns', 'strategy_returns']].plot()

# Calculate betas for all symbols against BTC
for sym in symbols:
    result = linregress(returns['BTCUSDT'].values, returns[sym].values)
    print(f'Beta for {sym} regressed on BTC is {result.slope}')