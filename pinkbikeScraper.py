import requests
import sys
import re
import pymongo
from bs4 import BeautifulSoup

client = pymongo.MongoClient("mongodb+srv://dbTest:<password>@cluster0.fsdva.mongodb.net/personal-site?retryWrites=true&w=majority")
db = client.test

URL = 'https://www.pinkbike.com/buysell/list/?lat=37.6806&lng=-122.4073&distance=101&category=2'    #local Trail
#URL = 'https://www.pinkbike.com/buysell/list/?lat=37.6806&lng=-122.4073&distance=101&category=1'   #local DH
#URL = 'https://www.pinkbike.com/buysell/list/?category=2'                                          #All Trail
#URL = 'https://www.pinkbike.com/buysell/list/?category=1'                                          #All DH
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

#result = soup.find(id='csid2882151')
#print (result.text.strip())
#print(result.prettify())
bikeElements = soup.find_all('div', class_="bsitem")
for bikeElement in bikeElements:
    
    bikeURL = bikeElement.find('li', class_='uImage').find('a', href=True)
    if None in (bikeURL):
        continue
    #print(bikeElement.text.strip())
    bikeId = bikeElement.get('id')
    bikeSpecs = bikeElement.find_all('div')
    for spec in bikeSpecs:
       print(spec.text.strip())
    break