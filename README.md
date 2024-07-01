# ByBitTrader
# FOLLOWED TUTORIAL: https://www.codearmo.com/python-tutorial/bybit-intro

*) DO NOT RUN ANY PLACE ORDER, DO NOT RUN ANY METHOD FROM ORDERS.py. Unless you are sure that you want to post/place the order. YOU CAN RUN ANY OTHER METHOD FROM ANYOTHER FILE.

1) Install Python 3.11.9 or a newer version
2) When you are installing choose to add PATH variable to python, tick the all options.
3) Install pycharm community edition
4) Import project
5) Set you API key and secret (previously generated on byBit, do not share those keys :p )
6) After importing, right click on virtualenv folder, click open in > terminal
7) Start running all pip install {packageName}
8) pip install datetime same for all required libraries, if you do mouse over on the error line it will show possible solutions, do pip install for all required libraries
9) you can run, not sure wich methods are working and wich ones dont.
10) DO NOT RUN ANY PLACE ORDER, DO NOT RUN ANY ORDER FILE OR METHOD FROM ORDERS.
11) YOU ARE READY TO GO.


###################  ORDERBOOK.PY EAMPLE OUTPUT:  #####################

2023-12-15  1702598400000  2317.30  2320.30  ...  2221.84  652138.56  1.473490e+09
2023-12-16  1702684800000  2221.84  2264.95  ...  2229.77  339317.06  7.615666e+08
2023-12-17  1702771200000  2229.77  2250.99  ...  2197.79  433176.87  9.626331e+08
2023-12-18  1702857600000  2197.79  2226.85  ...  2221.37  766471.27  1.662722e+09
2023-12-19  1702944000000  2221.37  2256.72  ...  2179.20  794217.52  1.749404e+09
...                   ...      ...      ...  ...      ...        ...           ...
2024-06-27  1719446400000  3369.67  3475.84  ...  3448.56  547417.17  1.874076e+09
2024-06-28  1719532800000  3448.56  3486.54  ...  3378.37  667790.70  2.286971e+09
2024-06-29  1719619200000  3378.37  3407.25  ...  3377.00  222377.79  7.535594e+08
2024-06-30  1719705600000  3377.00  3459.29  ...  3436.40  319986.61  1.087989e+09
2024-07-01  1719792000000  3436.40  3523.57  ...  3504.97  149082.01  5.201225e+08

[200 rows x 7 columns]
Collecting data starting 2024-07-01 15:00:00
Collecting data starting 2024-07-01 15:00:00
Getting Orderbook
Bid price - 3504.97 , quantity = 0.87
Bid price - 3504.93 , quantity = 0.18
Bid price - 3504.91 , quantity = 0.19
Bid price - 3504.85 , quantity = 0.82
Bid price - 3504.82 , quantity = 0.06
Bid price - 3504.79 , quantity = 1.13
Bid price - 3504.78 , quantity = 0.06
Bid price - 3504.77 , quantity = 0.12
Bid price - 3504.74 , quantity = 0.06
Bid price - 3504.73 , quantity = 0.29

############ WEBSOCKET.PY EAMPLE OUTPUT: #####################

{'asset': 'ETHUSDT', 'best_bid': 3505.83, 'bid_volume': 42.03, 'best_ask': 3505.84, 'ask_volume': 22.11}
12
{'asset': 'ETHUSDT', 'best_bid': 3505.83, 'bid_volume': 42.07, 'best_ask': 3505.84, 'ask_volume': 22.1}
18
{'asset': 'ETHUSDT', 'best_bid': 3505.83, 'bid_volume': 33.22, 'best_ask': 3505.84, 'ask_volume': 33.03}
38
{'asset': 'ETHUSDT', 'best_bid': 3505.83, 'bid_volume': 33.32, 'best_ask': 3505.84, 'ask_volume': 33.45}
52
{'asset': 'ETHUSDT', 'best_bid': 3505.83, 'bid_volume': 18.22, 'best_ask': 3505.84, 'ask_volume': 33.96}
73
{'asset': 'ETHUSDT', 'best_bid': 3505.83, 'bid_volume': 18.26, 'best_ask': 3505.84, 'ask_volume': 34.1}
83
{'asset': 'ETHUSDT', 'best_bid': 3505.83, 'bid_volume': 16.83, 'best_ask': 3505.84, 'ask_volume': 36.22}
93
{'asset': 'ETHUSDT', 'best_bid': 3505.83, 'bid_volume': 17.14, 'best_ask': 3505.84, 'ask_volume': 38.15}
105
{'asset': 'ETHUSDT', 'best_bid': 3505.83, 'bid_volume': 2.57, 'best_ask': 3505.84, 'ask_volume': 58.82}
116
{'asset': 'ETHUSDT', 'best_bid': 3505.83, 'bid_volume': 2.19, 'best_ask': 3505.84, 'ask_volume': 48.31}

################# BOLLINGERBANDS.PY OUTPUT:  ###########################################################

             lower_band       mid    close   upper_band
timestamp                                              
2024-07-01  3506.063839  3506.073  3506.07  3506.082161


###################### LONGSTRATEGY.PY OUTPUT   ################################################

Beta for ETH regressed on BTC is 1.0628553331371073
Beta for ETH regressed on BTC is 1.168369271637574
Longing 11683.69271637574 worth of BTC
Beta for BTCUSDT regressed on BTC is 1.0
Beta for ETHUSDT regressed on BTC is 1.0628553331371073
Beta for BNBUSDT regressed on BTC is 0.8114688886067646
Beta for XRPUSDT regressed on BTC is 0.9017983129299196
Beta for ADAUSDT regressed on BTC is 1.063164618432261
Beta for DOGEUSDT regressed on BTC is 1.1106586979787003
Beta for MATICUSDT regressed on BTC is 1.231524463841423
Beta for SOLUSDT regressed on BTC is 1.4208345546536434
Beta for DOTUSDT regressed on BTC is 1.0776377450461245
Beta for LTCUSDT regressed on BTC is 1.001855366340629
