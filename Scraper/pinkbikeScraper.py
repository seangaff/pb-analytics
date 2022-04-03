import requests
import sys
import re
import datetime
from datetime import datetime
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('/Users/seangaffney/Documents/Code/pb-analytics-616-firebase-adminsdk-5rw79-c5f78deb10.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

#URL = 'https://www.pinkbike.com/buysell/list/?lat=37.6806&lng=-122.4073&distance=101&category=2'       #local Trail
baseURL = 'https://www.pinkbike.com/buysell/list/?region=3&category=2'                                      #All Trail

def iterateSeach():
    page = requests.get(baseURL)
    soup = BeautifulSoup(page.content, 'html.parser')
    lastPage = int(soup.find('ul',class_="paging-middle centertext").find_all('li')[-1].text.strip())
    print(lastPage + " Total pages")
    print("-Iterating through search pages...")

def scrapeSearchPage(URL):
    print("-Scraping Search Page")
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    bikeElements = soup.find_all('div', class_="bsitem")
    # lastPage = int(soup.find('ul',class_="paging-middle centertext").find_all('li')[-1].text.strip())

    #Iterates through all bikes in a search result
    for bikeElement in bikeElements:
        scrapeElement(bikeElement)
        break

def scrapeElement(bikeElement):
    print(" -Scraping Element")
    pbID = bikeElement.get('id').replace("csid","")
    print("ID: " + pbID)
    bikeURL = "https://www.pinkbike.com/buysell/" + pbID

    bikeData = bikeElement.find_all('td')
    bikeSpecs = bikeData[1].find_all("div")
    #check for all necessary information
    if len(bikeSpecs) < 7:
        print(" Missing Specs Data")
        return
    title = bikeData[1].a.string
    condition = bikeSpecs[1].text.split(":",1)[1].strip()
    frameSize = bikeSpecs[2].text.split(":",1)[1].strip()
    wheelSize = bikeSpecs[3].text.split(":",1)[1].replace('"',"").strip()
    material = bikeSpecs[4].text.split(":",1)[1].strip()
    frontTravel = bikeSpecs[5].text.split(":",1)[1].strip()
    rearTravel = bikeSpecs[6].text.split(":",1)[1].strip()

    bikeInfo = bikeData[1].find_all("tr")
    location = bikeInfo[0].text.strip()
    # seller = bikeInfo[1].text.split(":")[1].split("|")[0].replace("Outside+", "").strip()
    seller = bikeInfo[1].a.text.replace("Outside+", "").strip()
    price = int(bikeInfo[2].text.replace("$","").split(" ")[0].strip())
    #if price is in CAD, rough conversion to USD
    if((bikeInfo[2].text.replace("$","").split(" ")[1].strip()) == "CAD"):
        price = price*0.8
    price = int(price)

    #get listing data from Bike's page by pbID
    bikePage = requests.get(bikeURL)
    bikeSoup = BeautifulSoup(bikePage.content, 'html.parser')   
    bikeDetails = bikeSoup.find_all("div",class_="buysell-details-column")[1].get_text(strip=True, separator='\n').splitlines()
    postDate = datetime.strptime((bikeDetails[1].split(" ")[0].replace("-"," ")), '%b %d %Y')
    repostDate = datetime.strptime((bikeDetails[3].split(" ")[0].replace("-"," ")), '%b %d %Y')
    if(bikeDetails[5] == "since"):
        forSale = bikeDetails[6]
        viewCount = int(bikeDetails[8].replace(",", ""))
        watchCount = int(bikeDetails[10].replace(",", ""))
    else:
        forSale = bikeDetails[5]
        viewCount = int(bikeDetails[7].replace(",", ""))
        watchCount = int(bikeDetails[9].replace(",", ""))

    
    #publish data as json to fireStore
    doc_ref = db.collection(u'trailEnduro').document(pbID)
    doc_ref.set({
        u'title': title,
        u'location': location,
        u'seller': seller,
        u'price_usd': price,
        u'spec': {
            u'condition': condition,
            u'frame_size': frameSize,
            u'wheel_size': wheelSize,
            u'material': material,
            u'front_travel': frontTravel,
            u'rear_travel': rearTravel
        },
        u'listing': {
            u'post_date': postDate,
            u'repost_date': repostDate,
            u'for_sale': forSale,
            u'view_count': viewCount,
            u'watch_count': watchCount,
        },
    })

# def scrapeListing():
#     print("Scraping Listing")

# def publishData():
#     print("Publishing Data")

if __name__ == '__main__':
    # iterateSeach()
    scrapeSearchPage(baseURL)