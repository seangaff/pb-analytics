import requests
import sys
import re
import datetime
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('/Users/seangaffney/Documents/Code/pb-analytics-616-firebase-adminsdk-5rw79-c5f78deb10.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

URL = 'https://www.pinkbike.com/buysell/list/?lat=37.6806&lng=-122.4073&distance=101&category=2'    #local Trail
#URL = 'https://www.pinkbike.com/buysell/list/?region=3&category=2'                                 #All Trail

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
bikeElements = soup.find_all('div', class_="bsitem")

for bikeElement in bikeElements:
    pbID = bikeElement.get('id').replace("csid","")
    print(pbID)
    bikeURL = "https://www.pinkbike.com/buysell/" + pbID
    bikeData = bikeElement.find_all('td')
    bikeSpecs = bikeData[1].find_all("div")

    title = bikeData[1].a.string
    condition = bikeSpecs[1].text.split(":",1)[1].strip()
    frameSize = bikeSpecs[2].text.split(":",1)[1].strip()
    wheelSize = bikeSpecs[3].text.split(":",1)[1].strip()
    Material = bikeSpecs[4].text.split(":",1)[1].strip()
    frontTravel = bikeSpecs[5].text.split(":",1)[1].strip()
    rearTravel = bikeSpecs[6].text.split(":",1)[1].strip()

    bikeInfo = bikeData[1].find_all("tr")
    location = bikeInfo[0].text.strip()
    seller = bikeInfo[1].text.split(":")[1].split("|")[0].strip()
    price = int(bikeInfo[2].text.replace("$","").split(" ")[0].strip())


    bikePage = requests.get(bikeURL)
    bikeSoup = BeautifulSoup(bikePage.content, 'html.parser')   
    bikeDetails = bikeSoup.find_all("div",class_="buysell-details-column")[1].get_text(strip=True, separator='\n').splitlines()

    postDate = bikeDetails[1]
    repostDate = bikeDetails[3]
    forSale = bikeDetails[6]
    viewCount = int(bikeDetails[8].replace(",", ""))
    watchCount = int(bikeDetails[10].replace(",", ""))

    doc_ref = db.collection(u'trailEnduro').document(pbID)
    doc_ref.set({
        u'title': title,
    })

    break

'''
class bikeScraper():
    def iterSeachPage():

    def scrapeSearchPage(URL):

    def scrapeElement():

    def scrapeListing():


if __name__ == '__main__':
    iterSearchPage(URL)
'''   