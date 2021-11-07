import requests
import sys
import re
#import pymongo
from bs4 import BeautifulSoup

#URL = 'https://www.pinkbike.com/buysell/list/?lat=37.6806&lng=-122.4073&distance=101&category=2'    #local Trail
URL = 'https://www.pinkbike.com/buysell/list/?region=3&category=2'                                 #All Trail

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
bikeElements = soup.find_all('div', class_="bsitem")

for bikeElement in bikeElements:
    pbId = bikeElement.get('id').replace("csid","")
    print(pbId)
    bikeURL = "https://www.pinkbike.com/buysell/" + pbId
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
    viewCount = int(bikeDetails[8])
    watchCount = int(bikeDetails[10])

    #break

'''
class bikeScraper():
    def iterateSeachPage():

    def scrapeSearchPage(URL):

    def scrapeBikeElement():

    def scrapeListing():


if __name__ == '__main__':

'''   