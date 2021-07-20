import requests
import shutil
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
# -*- coding: utf-8 -*-
 
from requests import get
 
url ="https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

response = get(url)
print(response.text[:500])

#Type is a great function that will tell us what 'type' a variable is. Here, response is a http.response object.
print(type(response))
 
if response.ok:
  html_soup = BeautifulSoup(response.text,features='html.parser')
  type(html_soup)
 
  #bookshelf = html_soup.find_all("div",{"class":"col-sm-6 product_main"})
  #print(type(bookshelf))
  url_1 ="https://books.toscrape.com/"
  url_2 ="media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg" 
  link  = urljoin(url_1,url_2)

  table = html_soup.find("table", {"class":"table table-striped"})
  results = table.find_all("td")
  title = html_soup.find("h1").text.strip()
  
  don=[]
  category = html_soup.find("li", {"class": "active"}).findPrevious("a")
  cat = category.text
  don.append(cat)

  if html_soup.find("div", {"id": "product_description"}):
     proddesc = html_soup.find("div", {"id": "product_description"}).findNext("p")
     product_description = proddesc.text
     don.append(product_description)
  else:
    product_description = "No description available"
    don.append(product_description)
  
  UPC = results[0].text.strip() #la methode .strip() enlève les espaces en début et en fin de mot.
  Product_type = results[1].text.strip()
  Price_excluding_tax = results[2].text.strip()
  Price_including_tax = results[3].text.strip()
  Tax = results[4].text.strip()
  Availability = results[5].text.strip()
  Numbers_of_review = results[6].text.strip()
 
  image_soup = html_soup.find("div",{"class":"item active"}).find("img")
  #image_src = image_soup.src
  image_src=image_soup["src"]

  image_response = get(link, stream=True)

  with open('img.png', 'wb') as out_file:
   shutil.copyfileobj(image_response.raw, out_file)
  del image_response

  stars=[]
  if html_soup.find("p", {"class": "star-rating One"}):
       review_rating = "1 étoile"
       stars.append(review_rating)
  elif html_soup.find("p", {"class": "star-rating Two"}):
       review_rating = "2 étoiles"
       stars.append(review_rating)
  elif html_soup.find("p", {"class": "star-rating Three"}):
       review_rating = "3 étoiles"
       stars.append(review_rating)
  elif html_soup.find("p", {"class": "star-rating Four"}):
       review_rating = "4 étoiles"
       stars.append(review_rating)
  elif html_soup.find("p", {"class": "star-rating Five"}):
       review_rating = "5 étoiles"
       stars.append(review_rating)
  else:
       review_rating = "Il n'y a pas de note"
       stars.append(review_rating)

  print(cat)
  print(title)
  print(review_rating)
  print(UPC)
  print(Product_type)
  print(Price_excluding_tax)
  print(Price_including_tax)
  print(Tax)
  print(Availability)
  print(Numbers_of_review)
  print(product_description)
  #print('Number of results', len(results))
 
 
def tableau(result):
    tab=[]
    for result in results:
         #result = results.find("td")
         tab.append(result)
         return tab
 
with open("donnees.csv", "w", encoding="utf-8") as fichier:
    writer = csv.writer(fichier)
 
j = len(results)
i = 0
with open("donnees.csv", "w", encoding="utf-8") as fichier:
    writer = csv.writer(fichier)
    while i < j:
        writer.writerow(results[i])
        i+=1


