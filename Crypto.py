import requests
from datetime import datetime
import csv
import time

url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd'
while True:
    response = requests.get(url)
    data = response.json()
    for datas in data:
        price = data[datas]['usd']
        print(f'{datas}: {price}')
        Time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_name = 'price_data.csv'
        with open(file_name, 'a', newline='', encoding='utf-8')as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow([Time])
            writer.writerow([datas, price])
        print('Done')
    time.sleep(60)
