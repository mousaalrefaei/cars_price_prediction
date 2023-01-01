from bs4 import BeautifulSoup , SoupStrainer
import requests
from time import sleep
import json
from datetime import datetime
import csv
import os


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1'
}

cookies = {"CONSENT": "YES+cb.20210720-07-p0.en+FX+410"}



countries = {"Deutschland": "D"}

brands = {'Mercedes-Benz':'/mercedes-benz','Volkswagen':'/volkswagen', 'BMW': '/bmw', 'Audi':'/audi', 'Ford':'/ford', 'Opel':'/opel', 'Skoda':'/skoda','Toyota':'/toyota','Renault':'/renault', 'Porsche':'/porsche', 'Alfa-Romeo':'/alfa-romeo', 'Chevrolet':'/chevrolet','Citroen':'/citroen', 'Cupra':'/cupra', 'Dacia':'/dacia', 'Daewoo': '/daewoo', 'Daihatsu':'/daihatsu', 'Dodge':'/dodge', 'Ferrari':'/ferrari', 'Fiat':'/fiat', 'Hyundai':'/hyundai', 'Honda':'/honda', 'Infiniti':'/infiniti', 'Isuzu':'/isuzu', 'Jaguar':'/jaguar', 'Jeep':'/jeep', 'Kia':'/kia', 'Lada':'/lada', 'Lamborghini':'/lamborghini', 'Land Rover':'/land-rover', 'Lexus': '/lexus' ,'Maybach':'/maybach', 'Mazda': '/mazda','Mini':'/mini', 'Mitsubishi':'/mitsubishi', 'Nissan':'/nissan', 'Peugeot':'/peugeot', 'Rolls-Royce':'/rolls-royce', 'Rover':'/rover', 'Saab':'/saab', 'SEAT':'/seat', 'smart':'/smart', 'Subaru':'/subaru','Suzuki':'suzuki', 'Tesla':'/tesla', 'Volvo':'/volvo','No brand': ''}

bodies = {'Kleinwagen': '1', 'Cabrio':'2','Coupe': '3', 'SUV/Gelandewagen':'4', 'Kombi':'5', 'Limousine':'6', 'Van/Kleinbus': '12', 'Transporter':'13', 'Sonstige': '7'}

fuels= {'Benzin':'B', 'Diesel':'D', 'Elektro':'E', 'Autogas':'L', 'Erdgas':'C', 'Hybrid(Elektro/Benzin)': '3', 'Hybrid(Elektro/Diesel':'3', 'Sonstige':'O'}

buyers ={'Handler':'D', 'Privat':'P'}

gears= {'Automatik':'A', 'Schaltgetriebe': 'M', 'Halbautomatik':'S'}

# power_type = {'KW':'kw', 'PS':'hp'}




cars_count = 0
cycle_counter = 0

columns= ['url', 'country', 'date', 'verkaufer', 'ort', 'modell', 'marke', 'price', 'Karosserieform', 'Zustand', 'Sitzplätze','Türen', 'Kilometerstand', 'Erstzulassung','Leistung', 'Getriebe', 'Hubraum', 'Kraftstoff', 'Kraftstoffverbrauch', 'CO₂-Emissionen', 'Schadstoffklasse', 'Umweltplakette', 'Außenfarbe', 'Farbe laut Hersteller','Farbe der Innenausstattung','Innenausstattung', 'Lackierung']


output_file = open('cars.csv', 'a+', newline='', encoding='utf8')
writer = csv.DictWriter(output_file,fieldnames=columns, extrasaction='ignore')
writer.writeheader()

if not os.path.isfile('visited_urls.json'):
  with open('visited_urls.json','w') as file:
    json.dump([],file)


def scraping(page, country, brand, body, fuel, gear, buyer):

  try:

    url = 'https://www.autoscout24.de/lst'+ brands[brand] +'?body='+ bodies[body] +'&sort=age&desc=0&cy=' + countries[country] + '&atype=C&ustate=N%2CU&fuel='+ fuels[fuel] +'&powertype=kw&gear='+ gears[gear] +'&custtype='+ buyers[buyer] +'&ocs_listing=include&search_id=f1h01j7njy&page=' + str(page)

    only_a_tags = SoupStrainer("a")

    response = requests.request("GET", url,headers=headers, cookies=cookies)

    soup = BeautifulSoup(response.text, 'html.parser', parse_only= only_a_tags)
    
    urls = []

    for url in soup.find_all('a'):

      if r'/angebote/' in str(url.get('href')):
        urls.append(url.get('href'))
        
    url_unique = [car for car in list(set(urls)) if car not in visited_urls]

    if len(url_unique) > 0:

      for URL in url_unique:

        link = 'https://www.autoscout24.de'+URL

        print(f'get list : cycle {cycle_counter} | country: {country} | {len(url_unique)} new URLs '+' '*50, end="\r")

        try:
          data= {}
          data['url'] = link
          data['country'] = country
          data['date'] = str(datetime.now())
          response = requests.request('GET',link, headers=headers,cookies=cookies)
          soup = BeautifulSoup(response.text,'html.parser')

          data["verkaufer"] = soup.find_all("div",attrs={"class":"VehicleOverview_itemText__V1yKT"})[5].text if soup.find_all("div",attrs={"class":"VehicleOverview_itemText__V1yKT"})[5].text else ''

          data["ort"] = soup.find("a",attrs={"class":"scr-link LocationWithPin_locationItem__pHhCa"}).text if soup.find("a",attrs={"class":"scr-link LocationWithPin_locationItem__pHhCa"}).text else ''

          data["version"] = soup.find("div",attrs={"class":"StageTitle_modelVersion__Rmzgd"}).text if soup.find("div",attrs={"class":"StageTitle_modelVersion__Rmzgd"}).text else ''

          data["modell"] = soup.find("span",attrs={"class":"StageTitle_model__pG_6i StageTitle_boldClassifiedInfo__L7JmO"}).text if soup.find("span",attrs={"class":"StageTitle_model__pG_6i StageTitle_boldClassifiedInfo__L7JmO"}).text else ''

          data["marke"] = soup.find("span",attrs={"class":"StageTitle_boldClassifiedInfo__L7JmO"}).text if soup.find("span",attrs={"class":"StageTitle_boldClassifiedInfo__L7JmO"}).text else ''

          data["price"] =  soup.find("span",attrs={"class":"StandardPrice_price__X_zzU"}).text.replace('€ ','').replace('.','').replace(',-1','').replace(',-','') if soup.find("span",attrs={"class":"StandardPrice_price__X_zzU"}).text.replace('€ ','').replace('.','').replace(',-1','').replace(',-','') else ''

          for key, value in zip(soup.find_all("dt"),soup.find_all("dd")):
            data[key.get_text(separator='-')] = value.get_text(separator='-')
          writer.writerow(data)
          visited_urls.append(URL)
          
        except Exception as e:
          print(e)
          pass
      
      print(f' cycle: {cycle_counter} brand: {brand}, body: {body}, fuel: {fuel}, buyer:  {buyer}, page: {page} / 20 , new urls: {len(url_unique)}')
    print(f'total cars scraped: {cars_count}')
  except Exception as e:
    print(e)



while True:
  with open('visited_urls.json') as file:
    visited_urls = json.load(file)

  if len(visited_urls) > 100000:
    visited_urls = []
  try:
    cycle_counter +=1
    for country in countries:
      for brand in brands:
        for body in bodies:
          for gear in gears:
            for fuel in fuels:
              for buyer in buyers:
                # for power in power_type:
                for page in range(1,21):
                  scraping(page, country, brand, body, fuel, gear, buyer)
                  cars_count = len(visited_urls)
                  with open("visited_urls.json", "w") as file:
                    json.dump(visited_urls, file)
                  print(f'the total scraped cars: {cars_count} ')
  except Exception as e:
    print(e)
