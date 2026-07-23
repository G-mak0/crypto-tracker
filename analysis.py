from datetime import datetime, timedelta
import csv
import pandas as pd
import os


df = pd.read_csv('crypto_raw.csv')
print(df.isna().sum())
df['timee'] = pd.to_datetime(df['date'], format='mixed')
df['Interval_time'] = df['timee'].diff()
print(df['Interval_time'].value_counts())
df['clean_retime'] = df.drop_duplicates(
    subset=['date'], keep='first', inplace=True)
print(df['clean_retime'].value_counts())
df['date'] = pd.to_datetime(df['date'], format='mixed')
df = df.set_index('date')
df = df.resample('D').mean()
df = df[['prices', 'Volume']]
print(df)
df.to_csv('crypto_daily.csv')

#   Calculate moving averages
df = pd.read_csv('crypto_daily.csv')
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
