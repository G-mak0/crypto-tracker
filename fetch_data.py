import requests
from datetime import datetime, timedelta
import csv
import pandas as pd
import os

# Retrieve 365 days of historical data
now = datetime.now().timestamp()
file_path = 'crypto_raw.csv'
if not os.path.exists(file_path):
    url = f'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=365'
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
    Unix = data['prices']
    Volume = data['total_volumes']
    for (date, prices), (_, volume) in zip(Unix, Volume):
        time = datetime.fromtimestamp(date/1000)
        with open("crypto_raw.csv", 'a', newline='', encoding='utf-8')as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            if f.tell() == 0:
                writer.writerow(["date", "prices", "Volume"])
            writer.writerow([time, prices, volume])
    print('Done1')


else:
    # Incremental update: Start from the last recorded date
    df = pd.read_csv('crypto_raw.csv')
    lastest_date = df['date'].iloc[-1]
    try:
        lastest_date_change = int(datetime.strptime(
            lastest_date, "%Y-%m-%d %H:%M:%S.%f").timestamp())
    except ValueError:
        try:
            lastest_date_change = int(datetime.strptime(
                lastest_date, "%Y-%m-%d %H:%M:%S").timestamp())
        except ValueError:
            try:
                lastest_date_change = int(datetime.strptime(
                    lastest_date, "%Y-%m-%d").timestamp())
            except Exception as exc:
                raise ValueError(
                    f"Unsupported date fromat: {lastest_date}")from exc
    new_start_date = lastest_date_change + 86400
    if new_start_date < now:
        url = f'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from={new_start_date}&to={now}'
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(data)
        Unix = data['prices']
        Volume = data['total_volumes']
        for (date, prices), (_, volume) in zip(Unix, Volume):
            time = datetime.fromtimestamp(date/1000)
            with open('crypto_raw.csv', 'a', newline='', encoding='utf-8')as f:
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                writer.writerow([time, prices, volume])
    else:
        print(f'Date is newest')

    print('Done2')
