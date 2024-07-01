#################### DOCUMENTATION ######################
# Bollinger Bands
import datetime

# is a popular technical analysis tool used by traders to identify potential breakouts in price and analyze price
# volatility. It is composed of three lines - a moving average line, an upper band, and a lower band. The upper and
# lower bands are usually set two standard deviations away from the moving average line. The moving average line serves
# as a benchmark for the stock or asset's price action, while the upper and lower bands act as support and
# resistance levels.

from pybit.unified_trading import HTTP
import pandas as pd
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


##########################      DATA COLLECTION     ##################################################
# For the purpose of this article, we will utilize daily ETHUSDT data. The data collection code will be replicated
# from this article. The Bollinger Bands will be computed using daily data to ensure ease of analysis. However, should
# there be a preference for a different time interval, the linked article can be consulted to make the necessary
# adjustments.
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


start = int(dt.datetime(2021, 1, 1).timestamp())

interval = 'D'
symbol = 'ETHUSDT'
df = pd.DataFrame()

counter = 1
while counter <= 30:
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

    counter += 1

##############   Calculating Bollinger Bands (based on previously obtained data)   ####################################
# After collecting the data, the next step is to calculate the Bollinger Bands. This can be done easily with the
# pandas_ta module, as demonstrated below. For this calculation, we have used a moving average length of 20 days along
# with a multiplier of 2. However, it is important to note that these parameters can be adjusted based on individual
# preferences and requirements. By experimenting with these parameters, users can obtain more insight and potentially
# more accurate results.

df[['lower_band', 'mid', 'upper_band']] = ta.bbands(df.close, length=20, std=2).iloc[:, :3]

print(df[-1:][['lower_band', 'mid', 'close', 'upper_band']])


##########     Visualize Bollinger Bands     ###########################################
# In the following section, we generate signals for both long and short positions based on the calculated Bollinger
# Bands. A short signal is triggered when the Bitcoin closing price is greater than the upper band, while a long signal
# is generated when the closing price falls below the lower band. This is because the Bollinger Bands strategy is based
# on mean reversion, which implies that prices are likely to revert to their mean after deviating too far from it.
# In this case, the mean is represented by the 14-day moving average.

df['short_signal'] = np.where(df.close > df.upper_band, 1, 0)
df['long_signal'] = np.where(df.close < df.lower_band, 1, 0)

## lets plot the most recent 100 days
df[['lower_band', 'mid', 'close', 'upper_band']].plot(style=['k--', 'k-', 'b-', 'k--'])

plt.plot(df[df.long_signal==1]['close'], '^g')
plt.plot(df[df.short_signal==1]['close'], 'vr')
plt.title('Bollinger Bands Entries')
plt.ylabel('ETH Price USDT')


# The Bollinger Bands demonstrated above generated sell signals throughout the bullish trend of 2021, leading to
# substantial losses for those who blindly followed the strategy. This is because in a trending market, such as the one
# observed in 2021, the price tends to surpass the upper band frequently, and the opposite for a bear market.
#
# As an exercise, readers can explore enhancing the above strategy by incorporating a filter, such as taking long
# positions only if it aligns with a longer-term trend.
#
# On the other hand, if a trader believes that the market is currently downwards trading, he may want to short when the
# upper band is reached as a potential way to make money in a bear market.


########################    SUPERTREND INDICATOR        #######################################################

# The Supertrend indicator is a technical analysis tool that uses a combination of moving averages and ATR
# (average true range) to identify the trend direction and generate buy and sell signals. The Supertrend formula
# involves two parameters, namely the period for ATR calculation and the multiplier. The ATR value is calculated based
# on the high, low, and closing prices of the security, and then multiplied by the multiplier to get the final value.
# The Supertrend line is plotted by adding the ATR value to the moving average for a bullish trend and subtracting the
# ATR value from the moving average for a bearish trend. The buy and sell signals are generated when the price crosses
# above or below the Supertrend line. The Supertrend is a popular indicator among traders and can be used in various
# trading strategies.

# DATA COLLECTION
# In order to prevent repetition we will use the same logic for data collection as shown in the Bollinger Bands article.
# For the purposes of this article we will take 4 hour candles for ETHUSDT to create the super-trend indicator.

start = int(dt.datetime(2021, 1, 1).timestamp())

interval = 240
symbol = 'ETHUSDT'
df = pd.DataFrame()

counter = 1
while counter <= 30:

    response = session.get_kline(category='linear',
                                 symbol=symbol,
                                 start=start,
                                 interval=interval).get('result')

    latest = format_data(response)

    if not isinstance(latest, pd.DataFrame):
        break

    start = get_last_timestamp(latest)

    time.sleep(0.01)

    df = pd.concat([df, latest])
    print(f'Collecting data starting {dt.datetime.fromtimestamp(start / 1000)}')

    if len(latest) == 1:
        break

    counter += 1

# To calculate the Supertrend indicator using pandas_ta, we'll first need to import the library. Once we have pandas_ta
# installed and imported, we can use the supertrend() function to calculate the indicator. We'll pass in the high, low,
# and close prices of ETHUSDT, along with a factor that determines the sensitivity of the indicator. Once the
# Supertrend values are calculated, we can plot them using matplotlib. We'll create a new figure and axis object,
# and use the plot() function to plot the Supertrend values against the date range of the security's prices.
# With just a few lines of code, we can quickly calculate and plot the Supertrend indicator for any coin we're
# interested in analyzing.

print("Printing chart")
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

########################## Super Trend Backtest  #####################################################
# In the following analysis, we will compute the simple returns for a buy-and-hold strategy on ETH. Additionally,
# we will evaluate the returns from a long-short strategy that relies on the SuperTrend indicator, where the direction
# is denoted as either 1 or -1, corresponding to long or short positions, respectively. To ensure that we avoid
# lookahead bias, we must shift the returns as demonstrated below, given that the high, low, and close values for a
# given period are not available until the end of the period.

df['return'] = df.close.pct_change()
df.dropna(subset=['return'], inplace=True)
df['strategy'] = df.direction * df['return'].shift(-1)
df.dropna(subset=['strategy'], inplace=True)

(df['strategy']+1).cumprod().plot(label='Super Trend')
(df['close']/ df.close[:1].values[0]).plot(label='Buy and Hold')
plt.title('SuperTrend Backtest')
plt.ylabel('Cumulative Returns')
plt.legend()

# As illustrated in the plot above, a buy-and-hold strategy appears to outperform the strategy of solely following the
# Supertrend indicator. It is also important to note that we haven't included fees. However, it is important to note
# that the Supertrend indicator is typically utilized in conjunction with other technical indicators or for
# establishing stop loss/take profit levels. We urge the reader to experiment with this indicator in tandem with other
# technical indicators to evaluate its effectiveness in their investment strategy.