 
import requests
import shutil
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
# -*- coding: utf-8 -*-
 
from requests import get
import os
 
url_category = "https://books.toscrape.com/catalogue/category/books/poetry_23/index.html"
 
response = get(url_category)

if response.ok:
    html_soup = BeautifulSoup(response.content, features='html.parser')
    type(html_soup)
 
category_objects = html_soup.find_all("div", {"class": "image_container"})
 
# Tableau book_link contenant les urls parcourues
book_link = []
 
# on affiche la suite d'url des différents livres d'une page
for category in category_objects:
    url_book = category.find('a')['href']
 
    # url_1 est l'url général du site Booktoscrap.com
    url_1 = "https://books.toscrape.com/catalogue/a/b/c/"
    url_2 = url_book
    link = urljoin(url_1, url_2)
    book_link.append(link)
 
    # Url Page produit
    product_page = link
    # print(product_page)
 
book_data = []
category_name = ""
 
for url in book_link:
    # On recherche les titres des différents livres d'une page du site booktoscrap.com
    response_book = get(url)
    #print(url)
 
    # Type is a great function that will tell us what 'type' a variable is. Here, response is a http.response_book object.
    #print(response_book)
 
    if response_book.ok:
        html_soup = BeautifulSoup(response_book.text, features='html.parser')
        type(html_soup)
 
        table = html_soup.find("table", {"class": "table table-striped"})
        results = table.find_all("td")
        title = html_soup.find("h1").text.strip()
 
        don = []
        category = html_soup.find("li", {"class": "active"}).findPrevious("a")
        cat = category.text
        category_name = cat
        don.append(cat)
 
 
        if html_soup.find("div", {"id": "product_description"}):
            proddesc = html_soup.find(
                "div", {"id": "product_description"}).findNext("p")
            product_description = proddesc.text
            don.append(product_description)
        else:
            product_description = "No description available"
            don.append(product_description)
 
        # la methode .strip() enlève les espaces en début et en fin de mot.
        UPC = results[0].text.strip()
        Product_type = results[1].text.strip()
        Price_excluding_tax = results[2].text.strip()
        Price_including_tax = results[3].text.strip()
        Tax = results[4].text.strip()
        Availability = results[5].text.strip()
        Numbers_of_review = results[6].text.strip()
 
        image_soup = html_soup.find("div", {"class": "item active"}).find("img")
        image_src = image_soup["src"]
        url_1 = "https://books.toscrape.com/a/b/"
        link = urljoin(url_1, image_src)
 
        image_response = get(link, stream=True)
 
        with open(UPC + '.png', 'wb') as out_file:
            shutil.copyfileobj(image_response.raw, out_file)
        del image_response
 
        stars = []
        if html_soup.find("p", {"class": "star-rating One"}):
            review_rating = "1 etoile"
            stars.append(review_rating)
        elif html_soup.find("p", {"class": "star-rating Two"}):
            review_rating = "2 etoiles"
            stars.append(review_rating)
        elif html_soup.find("p", {"class": "star-rating Three"}):
            review_rating = "3 etoiles"
            stars.append(review_rating)
        elif html_soup.find("p", {"class": "star-rating Four"}):
            review_rating = "4 etoiles"
            stars.append(review_rating)
        elif html_soup.find("p", {"class": "star-rating Five"}):
            review_rating = "5 etoiles"
            stars.append(review_rating)
        else:
            review_rating = "Il n'y a pas de note"
            stars.append(review_rating)
 
        book_data.append([product_page, UPC, title, Price_including_tax, Price_excluding_tax, Availability, Numbers_of_review, product_description,category,review_rating, image_src])
        headers = [ "product_page" ,"UPC", "title" , "Price_including_tax", "Price_excluding_tax" , "Availability" , "Numbers_of_review", "product_description" , "category" , "review_rating" ,  "image_src" ]
 
 
        with open(category_name + '.csv', mode='w', encoding= 'UTF-8-SIG') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(headers)  
            for data in book_data:
              writer.writerow(data)
 
