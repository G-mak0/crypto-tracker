import requests
from datetime import datetime, timedelta
import csv
import pandas as pd
import os

now = datetime.now().timestamp()
file_path = 'crypto.csv'
if not os.path.exists(file_path):

    # Thirty_days_age = int((datetime.now()-timedelta(days=30)).timestamp())
    url = f'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/?vs_currency=usd&days=30'

    response = requests.get(url)
    data = response.json()
    Unix = data['prices']
    for date, prices in Unix:
        time = datetime.fromtimestamp(date/1000)
        print(f'Date:{date},Prices:{prices}')
        with open("crypto.csv", 'a', newline='', encoding='utf-8')as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            if f.tell() == 0:
                writer.writerow(["date", "prices"])
            writer.writerow([time, prices])
    print('Done')

else:
    df = pd.read_csv('crypto.csv')
    df['new_Date'] = df['Date']
    # df['change'] = df['prices'].pct_change()
    lastest_date = df['new_Date'].iloc[-1]
    url = f'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&from={lastest_date}&to={datetime.now()}'
    # lastest_date_change = int(datetime.strptime(
    #    lastest_date, "%Y-%m-%d %H-:%M:%S").timestamp())
    # print(df['change'])
    # print(len(df))
    print(lastest_date)
