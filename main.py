import requests
from send_email import send_email
# import logging
# import time
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')
url = (f'https://newsapi.org/v2/everything?q=tesla&'
       f'sortBy=publishedAt&apiKey={api_key}')
# 890603a55bfa47048e4490069ebee18c
# 'https://finance.yahoo.com'

res = requests.get(url)
content = res.text
data = res.json()

receiver = os.getenv('RECEIVER')

message_body = ''
for index, art in enumerate(data['articles']):
    print(f'processing index {index}')
    if art['title'] is not None and art['description'] is not None \
            and art['url'] is not None:
        message_body = (message_body + art['title'] + '\n' + art['description']
                        + '\n' + art['url'] + '\n' + 80 * '~' + '\n')


print(dir(message_body))
email_status = send_email(message_body, 'auto news', receiver)

if email_status:
    print('Your email was sent successfully!')
else:
    print('Something went wrong, failed to send email...')


print('Thanks for choosing us, have a nice day!')
