import requests
import sys
import re
from datetime import datetime
from bs4 import BeautifulSoup

bikePage = requests.get("https://www.pinkbike.com/buysell/2999537/")
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