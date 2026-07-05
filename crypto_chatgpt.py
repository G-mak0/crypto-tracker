import requests

url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30'

response = requests.get(url)
data = response.json()

print(data)
