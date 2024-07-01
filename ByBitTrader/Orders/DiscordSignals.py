import aiohttp
import asyncio
import pandas as pd
import datetime as dt
from pybit.unified_trading import HTTP
import numpy as np
from discord import SyncWebhook

# Define the Discord webhook URL
url = 'https://discord.com/api/webhooks/1256388710497521694/JVFtBpb5sbk3araGeMMVcfjDF4vKmWA_KWBzNWgedP46GiFmPuVrW9oQZIy7IKq3o_mZ'
webhook = SyncWebhook.from_url(url)

# Initialize the Bybit API client
bb = HTTP(testnet=False)

# Set the ticker to be checked
ticker = 'ETHUSDT'

# Define the price thresholds
price_thresholds = {
    "low": 3398,
    "high": 3450
}


def construct_url(category, symbol, interval):
    return f'https://api.bybit.com/v5/market/kline?category={category}&symbol={symbol}&interval={interval}'


async def get_data(category, ticker, interval):
    url = construct_url(category=category, symbol=ticker, interval=interval)
    async with aiohttp.ClientSession() as session:
        response = await session.get(url, ssl=True)
        return await response.json()


def format_data(response):
    data = response.get('list', None)
    if not data:
        return pd.DataFrame()

    data = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data.set_index('timestamp', inplace=True)
    return data[::-1].apply(pd.to_numeric)


def check_price_signal(data, price_thresholds):
    if data.empty:
        return None
    latest_close = data['close'].iloc[-1]
    if latest_close < price_thresholds['low']:
        return f'ETHUSDT price is below {price_thresholds["low"]}: {latest_close} \U0001F911'
    elif latest_close > price_thresholds['high']:
        return f'ETHUSDT price is above {price_thresholds["high"]}: {latest_close} \U0001F911'
    return None


async def monitor_price():
    while True:
        response = await get_data(category='linear', ticker=ticker, interval=60)
        data = format_data(response)
        message = check_price_signal(data, price_thresholds)

        if message:
            webhook.send(message)
        else:
            print('No significant price movement detected.')

        # Sleep for a minute before checking again
        await asyncio.sleep(60)


# Run the main function
asyncio.run(monitor_price())