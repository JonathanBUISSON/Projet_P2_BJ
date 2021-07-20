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

book_link=[]
for category in category_objects:
    #on affiche la suite d'url des différents livres d'une page
    url_book = category.find('a')['href']
   
    #url_1 est l'url général du site Booktoscrap.com
    url_1="https://books.toscrape.com/"
    url_2= url_book
    link = urljoin(url_1,url_2)
    book_link.append(link)
    print(link)

for url in book_link:
  #On recherche les titres des différents livres d'une page du site booktoscrap.com
  table = html_soup.find("table", {"class":"table table-striped"})
  print(table)
  results = table.find("td")
  print(results)
  title = html_soup.find("h1").text.strip()

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
      
    
      #On a un tableau results qui contient les données recherchées avec des index allant de 0 à 6 
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

    #On affiche l'évaluation du nombre d'étoiles pour les livres
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
         star.append(review_rating)

#On affiche nos résultats dans la fenêtre IDLE
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

#Première manière d'écrire un csv
        
    #with open("donnees.csv", "w", encoding="utf-8") as fichier:
      #writer = csv.writer(fichier)
 
    j = len(results)
    i = 0
    with open("donnees.csv", "w", encoding="utf-8") as fichier:
       writer = csv.writer(fichier)
       while i < j:
           writer.writerow(results[i])
           i+=1

#Deuxième manière d'écrire un csv
    with open('Resultatcomplet.csv', newline='') as csvfile:
         spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
         for row in spamreader:
           print(', '.join(row))
           product_page_url, universal_product_code, title, Price_including_tax, Price_excluding_tax,
           number_available, product_description, category, review_rating, image_url

#Troisième manière d'écrire un csv
           
#Mettre des en-têtes au fichier csv
           
headers = ['Product_page_url', 'universal_product_code','title','Price_including_tax','Price_excluding_tax',
             'number_available', 'product_description', 'category', 'review_rating',' image_url']

for row in interator:
    with open('file.csv', 'a') as file_2:
        file_is_empty = os.stat('file.csv').st_size == 0
        writer = csv.writer(file_2, lineterminator='\n')
        if file_is_empty:
            writer.writerow(headers)
        writer.writerow(row)

