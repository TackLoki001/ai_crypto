import time
import requests
import pandas as pd
import datetime

while True:
    book = {}
    response = requests.get('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5')
    book = response.json()

    data = book['data']

    bids = pd.DataFrame(data['bids']).apply(pd.to_numeric, errors='ignore')
    bids.sort_values('price', ascending=False, inplace=True)
    bids = bids.reset_index(drop=True)
    bids['type'] = 0

    asks = pd.DataFrame(data['asks']).apply(pd.to_numeric, errors='ignore')
    asks.sort_values('price', ascending=True, inplace=True)
    asks = asks.reset_index(drop=True)
    asks['type'] = 1

    df = pd.concat([bids, asks])
    timestamp = datetime.datetime.now()

    df['quantity'] = df['quantity'].round(decimals=4)
    df['timestamp'] = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    if datetime.datetime.now().hour == 0:
        df.to_csv(f"./{timestamp.date()}-bithumb-orderbook.csv", index=False, header=True, mode='a')
        df.to_csv(f"./{timestamp.date() + datetime.timedelta(days=1)}-bithumb-orderbook.csv", index=False, header=True, mode='a')
    else:
        df.to_csv(f"./{timestamp.date()}-bithumb-orderbook.csv", index=False, header=True, mode='a')

    time.sleep(1)
