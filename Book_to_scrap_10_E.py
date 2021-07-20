import requests
import shutil
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
# -*- coding: utf-8 -*-
 
from requests import get
import os


def file(library):
    directory = os.path.dirname(library)
    if not os.path.exists("directory"):
        os.makedirs("directory")
     
url_category= "https://books.toscrape.com/catalogue/category/books/poetry_23/index.html"

response = get(url_category)
print(response.text[:500])
#Type is a great function that will tell us what 'type' a variable is. Here, response is a http.response object.
print(type(response))

if response.ok:
  html_soup = BeautifulSoup(response.text,features='html.parser')
  type(html_soup)
  print(html_soup)
  
category_objects = html_soup.find_all("div",{"class":"image_container"})

#Tableau book_link contenant les urls parcourues
book_link=[]

#on affiche la suite d'url des différents livres d'une page
for category in category_objects:
    url_book = category.find('a')['href']
   
    #url_1 est l'url général du site Booktoscrap.com
    url_1="https://books.toscrape.com/"
    url_2= url_book
    link = urljoin(url_1,url_2)
    book_link.append(link)
    
    #Url Page produit
    product_page=link
    print(product_page)


for url in book_link:
   #On recherche les titres des différents livres d'une page du site booktoscrap.com
   #table = html_soup.find("li", "class = col-xs-6 col-sm-4 col-md-3 col-lg-3")
   rex = html_soup.find_all("table", {"class":"table table-striped"})
   

for rex in book_link:
   #print(rex)
   #results = html_soup.find("a")["href"]
   results = str(rex.find("td"))
   print(results)
   print(type(results))
   #print(results)
   title = html_soup.find("h1").text.strip()
   print(title)

#on crée un tableau "don" de données qui regroupent les différentes catégories de livres
   don=[]
   category = html_soup.find("li", {"class": "active"}).findPrevious("a")
   cat = category.text
   don.append(cat)

#On affiche la description des livres dans le tableau "prod":
   prod=[]
   if html_soup.find("div", {"id": "product_description"}):
     proddesc = html_soup.find("div", {"id": "product_description"}).findNext("p")
     product_description = proddesc.text
     prod.append(product_description)
   else:
     product_description = "No description available"
     prod.append(product_description)

   
   product_page = link

   UPC = results[0].strip() #La méthode .strip() enlève les espaces en début et en fin de mot.
   Product_type = results[1].strip()
   Price_excluding_tax = results[2].strip()
   Price_including_tax = results[3].text.strip()
   Tax = results[4].text.strip()
   Availability = results[5].text.strip()
   Numbers_of_review = results[6].text.strip()

   image_soup = html_soup.find("div",{"class":"item active"}).find("img")
   image_src = image_soup["src"]

   image_response = get (link, stream = True)

   with open("img.png", "wb") as out_file:
      shutil.copyfileobj(image_response.raw, p=out_file)
   del image_response

   stars=[]
   if html_soup.find("p",{"class": "star-rating One"}):
      review_rating = "1 étoile"
      stars.append(review_rating)
   elif html_soup.find("p",{"class":"star-rating Two"}):
      review_rating = "2 étoiles"
      stars.append(review_rating)
   elif html_soup.find("p",{"class":"star-rating Three"}):
       review_rating = "3 étoiles"
       stars.append(review_rating)
   elif html_soup.find("p",{"class":"star-rating Four"}):
      review_rating = "4 étoiles"
      stars.append(review_rating)
   elif html_soup.find("p",{"class": "star-rating Five"}):
       review_rating = "5 étoiles"
       stars.append(review_rating)
   else:
       review_rating="Il n'y a pas de note"
       stars.append(review_rating)

   print(product_page)
   print(cat)
   print(review_rating)
   print(UPC)
   print(Product_type)
   print(Price_excluding_tax)
   print(Price_including_tax)
   print(Tax)
   print(Availability)
   print(Numbers_of_review)
   print(product_description)
   print("Number of results", len(results))

   def tableau(result):
     tab=[]
     for result in results:
      tab.append(result)
     return tab

   with open("donnees.csv", "w", encoding = "utf-8") as fichier:
     writer = csv.writer(fichier)

   j=len(results)
   i=0
   with open("donnees.csv","w",encoding = "utf-8") as fichier:
      writer =csv.writer(fichier)
      while i<j:
         writer.writerow(results[i])
         i+=1
     
 



