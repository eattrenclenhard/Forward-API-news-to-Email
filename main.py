import requests

api_key = input('API key for newsapi.org?\n')
url = ('https://newsapi.org/v2/everything?q=tesla&'
       'sortBy=publishedAt&apiKey={api_key}')
# 890603a55bfa47048e4490069ebee18c
# 'https://finance.yahoo.com'

res = requests.get(url)
content = res.text
data = res.json()

for art in data['articles']:
    print(art['title'])
    print(art['description'])
