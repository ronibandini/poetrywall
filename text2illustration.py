# Poetry Wall
# Text 2 illustration example
# Roni Bandini, Buenos Aires, March 2023

# Poetry Wall
# text 2 illustration example 
# Roni Bandini, Buenos Aires, March 2023

import sys
import openai
import requests

openai.api_key=""

def img_gen(query):
	response = openai.Image.create(
  		prompt=query,
  		n=1,
  		size="512x512"
	)
	return response['data'][0]['url']


query="Commodore 64 made of gold"

res = img_gen(query)

img_data = requests.get(res).content
with open('test.jpg', 'wb') as handler:
    handler.write(img_data)
