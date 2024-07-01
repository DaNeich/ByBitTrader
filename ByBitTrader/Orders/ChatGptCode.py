import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

# Bybit API endpoints and credentials
API_URL = "https://api.bybit.com"
key = 'YOUR_SECRET'
secret = 'YOUr_API_KEY'


def fetch_historical_data(symbol, interval='1h', limit=200):
    try:
        endpoint = f"{API_URL}/v2/public/kline/list"
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit,
        }
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json()
        if 'result' not in data:
            raise ValueError('Result not found in API response')

        df = pd.DataFrame(data['result'])
        df['timestamp'] = pd.to_datetime(df['open_time'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df['close'] = df['close'].astype(float)
        return df

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

    except (KeyError, ValueError) as e:
        print(f"Error parsing JSON data: {e}")
        return None


def calculate_bollinger_bands(prices, window_size=20, num_std_dev=2):
    rolling_mean = prices.rolling(window=window_size).mean()
    rolling_std = prices.rolling(window=window_size).std()
    upper_band = rolling_mean + num_std_dev * rolling_std
    lower_band = rolling_mean - num_std_dev * rolling_std
    return lower_band.dropna(), upper_band.dropna()


def predict_prices(symbol, forecast_hours=2):
    # Fetch historical data
    historical_data = fetch_historical_data(symbol)
    if historical_data is None or historical_data.empty:
        return None, None

    prices = historical_data['close']

    # Calculate Bollinger Bands
    lower_band, upper_band = calculate_bollinger_bands(prices)

    # Fit linear regression to predict prices
    X = np.arange(len(prices)).reshape(-1, 1)
    model = LinearRegression()
    model.fit(X, prices)

    # Predict prices for the next forecast_hours hours
    future_hours = np.arange(len(prices), len(prices) + forecast_hours).reshape(-1, 1)
    future_prices = model.predict(future_hours)
    predicted_prices = pd.Series(future_prices, index=pd.date_range(prices.index[-1], periods=forecast_hours, freq='H'))

    # Predicted lower and higher prices
    predicted_lower_price = predicted_prices.min()
    predicted_higher_price = predicted_prices.max()

    return predicted_lower_price, predicted_higher_price


if __name__ == "__main__":
    symbol = 'ETHUSDT'
    lower_price, higher_price = predict_prices(symbol)
    if lower_price is not None and higher_price is not None:
        print(f"Predicted Lower Price for {symbol} within next 2 hours: {lower_price}")
        print(f"Predicted Higher Price for {symbol} within next 2 hours: {higher_price}")
    else:
        print("Prediction failed. Check logs for details.")