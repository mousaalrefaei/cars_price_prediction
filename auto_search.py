
### to be used after the price prediction to find similar cars on autoscout24 website ###

from bs4 import BeautifulSoup, SoupStrainer
import requests

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


def search_result(brand, model, type, year_from, year_to, km_from, km_to, area_range, area, fuel, gear, price_from, price_to, buyer, power_from, power_to):

  url = 'https://www.autoscout24.de/lst/'+ brand + '/'+ model +'/bt_'+ type +'?fregfrom='+ str(year_from) +'&fregto='+ str(year_to) + '&kmfrom='+ str(km_from) +'&kmto='+ str(km_to) +'&sort=standard&desc=0&cy=D&zipr=' + str(area_range) +'&zip='+ area +'&atype=C&ustate=N%2CU&fuel='+ fuel +'&powertype=kw&powerfrom='+ str(power_from) +'&powerto='+ str(power_to) +'&gear='+ gear +'&custtype='+ buyer +'&bcol=11&pricefrom='+ str(price_from) +'&priceto='+ str(price_to) +'&ocs_listing=include&search_id=25v5tmj582v&page=1'

  #url = 'https://www.autoscout24.de/lst/'+ brand + '/'+ model +'/'+ color +'?fregfrom='+ str(year_from) +'&fregto='+ str(year_to) + '&kmfrom='+ str(km_from) +'&kmto='+ str(km_to) +'&sort=standard&desc=0&cy=D&zipr=' + str(area_range) +'&zip='+ area +'&atype=C&ustate=N%2CU&fuel='+ fuel +'&powertype=kw&powerfrom='+ str(power_from) +'&powerto='+ str(power_to) +'&gear='+ gear +'&custtype='+ buyer +'&bcol=11&pricefrom='+ str(price_from) +'&priceto='+ str(price_to) +'&ocs_listing=include&search_id=25v5tmj582v&page=1'

  only_a_tags = SoupStrainer("a")

  response = requests.request("GET", url,headers=headers, cookies=cookies)

  soup = BeautifulSoup(response.text, 'html.parser', parse_only= only_a_tags)
  urls=[]
  search = {}
  for url in soup.find_all('a'):
    if r'/angebote/' in str(url.get('href')):
      urls.append(url.get('href'))
  for url in urls:
    link = 'https://www.autoscout24.de' + url
    try:
      data ={}

      data['url'] = link

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
      search[url]= data
    except Exception as e:
      #print(e)
      pass
  return search


# the following information are for trying the function:

# brand= 'volkswagen'
# model = 'passat-(alle)'
# color =  ''   #'bc_weiß'
# year_from= 1977
# year_to = 2022
# km_from= 1000
# km_to = 100000
# area_range = 400
# area = 'Essen'
# fuel = 'B'
# gear = 'M'
# price_from = 500
# price_to = 100000
# buyer = ''   #'D'
# power_from = 100
# power_to = 500
