import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.flipkart.com/search?q=mobile&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_na&as-pos=1&as-type=RECENT&suggestionId=mobile%7CMobiles&requestId=26fb0b9a-dc4d-4190-a9c0-22299a78fa9f&as-searchtext=mobiles'

req = requests.get(url)

content = BeautifulSoup(req.content,'html.parser')

print(content)