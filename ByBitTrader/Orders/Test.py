from pybit.unified_trading import WebSocket
from datetime import datetime, timedelta
import numpy as np

# Initialize pybit WebSocket client
key = 'YOUR_SECRET'
secret = 'YOUr_API_KEY'

public = WebSocket(channel_type='linear', testnet=False)
private = WebSocket(channel_type='private',
                    api_key=key,
                    api_secret=secret,
                    testnet=False)

ws = private


# Function to fetch historical data
def fetch_historical_data(symbol, start=None, end=None):
    if not start:
        start = int((datetime.utcnow() - timedelta(days=1)).timestamp())
    if not end:
        end = int(datetime.utcnow().timestamp())

    params = {
        'symbol': symbol,
        'from': start,
        'to': end,
        'interval': '1',
    }

    # Make API call to fetch historical data
    response = ws.kline_stream(params, ws)

    if response['ret_msg'] == 'OK':
        return response['result']
    else:
        print(f"Error fetching data: {response}")
        return None


# Function to calculate moving average
def moving_average(data, window_size):
    weights = np.repeat(1.0, window_size) / window_size
    return np.convolve(data, weights, 'valid')


# Function to predict lowest and highest prices
def predict_lowest_highest_prices(data, current_price):
    window_size = 20  # Adjust as needed
    std_deviation = np.std(data[-window_size:])
    predicted_lowest_price = current_price - std_deviation
    predicted_highest_price = current_price + std_deviation
    return predicted_lowest_price, predicted_highest_price


# Main function
def main():
    symbol = 'ETHUSDT'

    # Fetch historical data for last 24 hours
    historical_data = fetch_historical_data(symbol)

    if not historical_data:
        return

    # Extract closing prices
    closing_prices = np.array([float(entry['close']) for entry in historical_data])

    # Calculate simple moving average (SMA)
    sma_window_size = 50  # Example window size for SMA
    sma = moving_average(closing_prices, sma_window_size)

    # Predict next price using SMA (example)
    next_price_prediction = sma[-1]  # Replace with your prediction model

    # Predict lowest and highest prices within next 24 hours
    current_price = closing_prices[-1]
    predicted_lowest_price, predicted_highest_price = predict_lowest_highest_prices(closing_prices, current_price)

    # Print results
    print(f"Current Price (ETHUSDT): {current_price}")
    print(f"Predicted Next Price (using SMA): {next_price_prediction}")
    print(f"Predicted Lowest Price in Next 24 Hours: {predicted_lowest_price}")
    print(f"Predicted Highest Price in Next 24 Hours: {predicted_highest_price}")


if __name__ == "__main__":
    main()