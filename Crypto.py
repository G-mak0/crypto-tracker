import requests
from datetime import datetime, timedelta
import csv
import pandas as pd
import os

now = datetime.now().timestamp()
file_path = 'crypto.csv'
if not os.path.exists(file_path):

    # Thirty_days_age = int((datetime.now()-timedelta(days=30)).timestamp())
    url = f'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=365'

    response = requests.get(url)
    data = response.json()
    Unix = data['prices']
    for date, prices in Unix:
        time = datetime.fromtimestamp(date/1000)
        # print(f'Date:{date},Prices:{prices}')
        with open("crypto.csv", 'a', newline='', encoding='utf-8')as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            if f.tell() == 0:
                writer.writerow(["date", "prices"])
            writer.writerow([time, prices])
    print('Done1')
    df = pd.read_csv('crypto.csv')
else:
    df = pd.read_csv('crypto.csv')
    # df['change'] = df['prices'].pct_change()
    # print(df['change'])
    lastest_date = df['date'].iloc[-1]
    try:
        lastest_date_change = int(datetime.strptime(
            lastest_date, "%Y-%m-%d %H:%M:%S.%f").timestamp())
    except:
        lastest_date_change = int(datetime.strptime(
            lastest_date, "%Y-%m-%d %H:%M:%S").timestamp())
    url = f'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from={lastest_date_change}&to={now}'
    response = requests.get(url)
    data = response.json()
    Unix = data['prices']
    for date, prices in Unix:
        # print(f'Date:{date},Prices:{prices}')
        time = datetime.fromtimestamp(date/1000)
        with open('crypto.csv', 'a', newline='', encoding='utf-8')as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow([time, prices])
    print('Done2')
    df = pd.read_csv('crypto.csv')
df['MA7'] = df['prices'].rolling(window=7).mean()
df['MA25'] = df['prices'].rolling(window=25).mean()
# df['MA200'] = df['prices'].rolling(window=200).mean()
df['MA7_prices'] = df['MA7'].shift(1)
df['MA25_prices'] = df['MA25'].shift(1)
# df['MA200_prices'] = df['MA200'].shift(1)
df['cross_points_up'] = (df['MA7_prices'] <
                         df['MA25_prices']) & (df['MA7'] > df['MA25'])
df['cross_points_down'] = (df['MA7_prices'] >
                           df['MA25_prices']) & (df['MA7'] < df['MA25'])

print(df[df['cross_points_up']]['date'],
      [df[df['cross_points_up']]['prices']])

print(df[df['cross_points_down']]['date'],
      [df[df['cross_points_down']]['prices']])
df['after24'] = df['prices'].shift(-24)
df['change_pct'] = ((df['after24'] - df['prices']) / df['prices']) * 100
print(df[df['cross_points_up']][['prices', 'after24', 'change_pct']])
