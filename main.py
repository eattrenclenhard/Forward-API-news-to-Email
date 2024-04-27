import requests
from send_email import send_email
# import logging
# import time
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
topic = 'tesla'
url = (f'https://newsapi.org/v2/everything?q={topic}&'
       f'sortBy=publishedAt&apiKey={API_KEY}')
# 890603a55bfa47048e4490069ebee18c
# 'https://finance.yahoo.com'
params = {'language': 'en'}

res = requests.get(url, params)
content = res.text
data = res.json()

receiver = os.getenv('RECEIVER')

message_body = ''
for index, art in enumerate(data['articles'][:20]):
    print(f'processing index {index}')
    if art['title'] is not None and art['description'] is not None \
            and art['url'] is not None:
        message_body = (message_body + f'News {index}:' + art['title'] + '\n'
                        + art['description'] + '\n' + art['url']
                        + '\n' + 80 * '~' + '\n')


message_subject = "Today's news"
email_status = send_email(message_body, message_subject, receiver)

if email_status:
    print('Your email was sent successfully!')
else:
    print('Something went wrong, failed to send email...')


print('Thanks for choosing us, have a nice day!')
