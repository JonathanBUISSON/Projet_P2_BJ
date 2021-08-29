import shutil
from requests import get
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

def get_categories(url_standard):
    home_response = get(url_standard)
    if home_response.ok:
        home_html_soup = BeautifulSoup(home_response.content, features='html.parser')
        v = home_html_soup.select(".nav ul li a")
    return v

def get_objects(category_url):
    url_category = "https://books.toscrape.com/" + category_url['href']
    response = get(url_category)
    objects=[]
    if response.ok:
        html_soup = BeautifulSoup(response.content, features='html.parser')  
        obj = html_soup.find_all("div", {"class": "image_container"})
        for book in obj:
            book_url = get_book_link(book)# récupère l'url de chaque livre
            objects.append(book_url)
        next_page = html_soup.find('li', class_='next')
        while next_page:
            if 'index.html' in url_category:
                url_category = url_category.replace('index.html', next_page.find('a')['href'])
            elif 'page-' in url_category:
                url_category = url_category[:-6].replace('page', next_page.find('a')['href'])
            if url_category[-1] == "-":
                url_category = url_category[:len(url_category) - 1]
            response = get(url_category)
            soup = BeautifulSoup(response.content, features='html.parser')
            obj = html_soup.find_all("div", {"class": "image_container"})
            for book in obj:
                book_url = get_book_link(book)# récupère l'url de chaque livre
                objects.append(book_url)
            next_page = soup.find('li', class_='next')
    return objects

def get_book_link(book):
    url_book = book.find('a')['href']
    #url_1 est l'url général du site Booktoscrap.com
    url_1 = "https://books.toscrape.com/catalogue/a/b/c/"
    #on écrit /a/b/c pour remplacer les trois petits points qui sont écrits avant url_book.
    url_2 = url_book   #urls partielles.
    link = urljoin(url_1, url_2) #On utilise urljoin pour créer des urls complètes.
    return link

def get_book_infos(url_of_book):
    response_book = get(url_of_book) 
    if response_book.ok:
        html_soup = BeautifulSoup(response_book.content, features='html.parser')
        table = html_soup.find("table", {"class": "table table-striped"}) #On pointe vers l'élément recherché.
        results = table.find_all("td") #Parmi les tags "td" on dit cherche moi tous les tags td (d'ou le find.all).
        title = html_soup.find("h1").text.strip() #Pour le titre, on cherche le tag "h1"
        if html_soup.find("div", {"id": "product_description"}):
            proddesc = html_soup.find("div", {"id": "product_description"}).findNext("p")
            product_description = proddesc.text
        else:
            product_description = "No description available"
        #print(product_description)
        #On utilise un tableau results avec index (et l'index en python commence à zéro) et on utilise la methode .strip() qui enlève les espaces en début et en fin de mot.
        UPC = results[0].text.strip()  
        Product_type = results[1].text.strip()
        Price_excluding_tax = results[2].text.strip()
        Price_including_tax = results[3].text.strip()
        Tax = results[4].text.strip()
        Availability = results[5].text.strip()
        Numbers_of_review = results[6].text.strip()
              
        image_soup = html_soup.find("div", {"class": "item active"}).find("img") #On crée un objet image.soup qui permet de trouver les images recherchées.
        image_src = image_soup["src"] #puis on indique avec un objet image_src que l'objet_soup est repéré par le tag "src" (qui veut dire source).
        url_1 = "https://books.toscrape.com/a/b/"
        image_url = urljoin(url_1, image_src) #on récupère une (des) url(s) complète(s)
        
        image_response = get(image_url, stream=True) #Avec image_response on recherche les urls complètes des images avec "get"

        with open(UPC + '.png', 'wb') as out_file: #On stocke les images dans le dossier contenant ce programme et on fait varier les images en même temps que le UPC qui est un format en dynamique (on aurait pu choisir un autre des paramètres du results cela aurait été pareil). et la terminaison ce sont des ".png"
            shutil.copyfileobj(image_response.raw, out_file) # shutil.copyfile() method in Python est utilisé pour copier le contenu d'un fichier source vers un fichier destination.
        del image_response # del permet d'effacer image_response pour ne pas tout le temps avoir la même image.
        
        stars = [] #On crée un tableau vide stars qui contiendra en fonction des tag "p" rencontrés et de la classe si le livre est côté à 1 ou plusieurs étoiles voire à aucune étoile (dernière condition).
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

        #On remplit le tableau book_data avec les données demandés par SAM et on rajoute un headers qui contient les en-têtes, il faut que les données correspondent dans le même ordre !
        return [UPC, title, Price_including_tax, Price_excluding_tax, Availability, Numbers_of_review, product_description,review_rating, image_url]

def fonction_csv(data_of_books,category_name):
    headers = [ "UPC", "title" , "Price_including_tax", "Price_excluding_tax" , "Availability" , "Numbers_of_review", "product_description" , "review_rating" ,  "image_url" ]
    with open(category_name + '.csv', mode='w',newline='', encoding= 'UTF-8-SIG') as csv_file:
        writer = csv.writer(csv_file, delimiter=';') #On met un délimiteur pour séparer les informations écrites dans les différents csv pour chacune des données recueillies.
        writer.writerow(headers)  #On écrit les en-têtes.
        for data in data_of_books:  #Pour les données dans Book_data écrire les data (données).
            writer.writerow(data)


if __name__ == '__main__':
    url_home = "http://books.toscrape.com"
    category_urls = get_categories(url_home) #liste de toutes les catégories
    for category in category_urls:
        cat = category.text.strip()
        book_objects = get_objects(category) #ramène tous les livres de cette catégorie
        books_data=[]
        for book_url in book_objects:
            book_infos=get_book_infos(book_url) #récupère toutes les informations de chaque livre
            books_data.append(book_infos) #remplit un tableau vide books_data avec les données récoltées.
        fonction_csv(books_data,cat)
            
            

