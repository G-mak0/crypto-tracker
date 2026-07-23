import requests
from datetime import datetime, timedelta
import csv
import pandas as pd
import os

# Retrieve 365 days of historical data
now = datetime.now().timestamp()
file_path = 'crypto.csv'
if not os.path.exists(file_path):
    url = f'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=365'
    response = requests.get(url)
    data = response.json()
    Unix = data['prices']
    Volume = data['total_volumes']
    for (date, prices), (_, volume) in zip(Unix, Volume):
        time = datetime.fromtimestamp(date/1000)
        with open("crypto.csv", 'a', newline='', encoding='utf-8')as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            if f.tell() == 0:
                writer.writerow(["date", "prices", "Volume"])
            writer.writerow([time, prices, volume])
    print('Done1')

    df = pd.read_csv('crypto.csv')


else:
    # Incremental update: Start from the last recorded date
    df = pd.read_csv('crypto.csv')
    lastest_date = df['date'].iloc[-1]
    try:
        lastest_date_change = int(datetime.strptime(
            lastest_date, "%Y-%m-%d %H:%M:%S.%f").timestamp())
    except:
        lastest_date_change = int(datetime.strptime(
            lastest_date, "%Y-%m-%d %H:%M:%S").timestamp())

    new_start_date = lastest_date_change + 86400
    if new_start_date < now:
        url = f'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from={new_start_date}&to={now}'
        response = requests.get(url)
        data = response.json()
        print(data)
        Unix = data['prices']
        Volume = data['total_volumes']
        for (date, prices), (_, volume) in zip(Unix, Volume):
            time = datetime.fromtimestamp(date/1000)
            with open('crypto.csv', 'a', newline='', encoding='utf-8')as f:
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                writer.writerow([time, prices, volume])
    else:
        print(f'Date is newest')

    print(df.isna().sum())
    df['timee'] = pd.to_datetime(df['date'], format='mixed')
    df['Interval_time'] = df['timee'].diff()
    print(df['Interval_time'].value_counts())
    df['clean_retime'] = df.drop_duplicates(
        subset=['date'], keep='first', inplace=True)
    print(df['clean_retime'].value_counts())
    df['date'] = pd.to_datetime(df['date'], format='mixed')
    df = df.set_index('date')
    Daily_ = df.resample('D').mean()
    print(Daily_)
    df.to_csv('crypto.csv')
    print('Done2')

    # Calculate moving averages
    df = pd.read_csv('crypto.csv')
df['MA7'] = df['prices'].rolling(window=7).mean()
df['MA25'] = df['prices'].rolling(window=25).mean()
df['MA20'] = df['Volume'].rolling(window=20).mean()
df['MA7_prices'] = df['MA7'].shift(1)
df['MA25_prices'] = df['MA25'].shift(1)
# Identify crossover signals
df['cross_points_up'] = (df['MA7_prices'] <
                         df['MA25_prices']) & (df['MA7'] > df['MA25']) & (df['Volume'] > df['MA20'])
df['cross_points_down'] = (df['MA7_prices'] >
                           df['MA25_prices']) & (df['MA7'] < df['MA25']) & (df['Volume'] < df['MA20'])

print(df[df['cross_points_up']]['date'],
      [df[df['cross_points_up']]['prices']],
      df[df['cross_points_up']]['Volume'])

print(df[df['cross_points_down']]['date'],
      [df[df['cross_points_down']]['prices']],
      df[df['cross_points_down']]['Volume'])
# Backtesting: Calculate the percentage change after 24 hours
df['after24'] = df['prices'].shift(-24)
df['change_pct'] = ((df['after24'] - df['prices']) / df['prices']) * 100
print(df[df['cross_points_up']][['prices', 'after24', 'change_pct']])
