# Extracting category + book following data:

# check a chosen category and extract it
# url from all books in it
# extract whole infos with the assistance of step_1_scraping_one_book

# writing down infos in a .csv

import requests
from bs4 import BeautifulSoup
import csv
import time
from tqdm import tqdm


def scraping_books_category(soup):
	links = []

	books = soup.select("article.product_pod") # <-- name html

	for book in books:
		href = book.find("a")["href"] #<-- tag html
		href = href.split("/")
		links.append("http://books.toscrape.com/catalogue/" + href[-2] + "/" + href[-1])

	return links





def find_products_url_by_category(url_categ):
    # 20 books by page
    response = requests.get(url_categ)
    links = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        is_pagination = soup.find("ul", {"class": "pager"})

        if is_pagination:
            nbPages = is_pagination.find('li', {"class": "current"}).text.strip()
            nbPages = int(nbPages[-1:])

            if nbPages:
            	for i in range(1, nbPages + 1):
            		url = url_categ.replace("index.html", "page-" + str(i) + ".html")

            		response = requests.get(url)

            		if (response.status_code == 200):
            			soup = BeautifulSoup(response.text, "html.parser")

            			links += scraping_books_category(soup)
            		time.sleep(0.025) #avoiding blacklist

            else:
            	
            	links = scraping_books_category(soup)

    return links







def scrap_one_book(url):
	book_data = {"product_page_url": url}

	response = requests.get(book_data["product_page_url"])

	if response.status_code == 200:
		soup = BeautifulSoup(response.text, "html.parser")

	# extracting universal_product_code (upc) / price_exculding_tax / price_inculding_tax from book_table / availability

		data = soup.findAll("tr")

		for datum in data:
			datum_name = datum.find("th").text
			datum_value = datum.find("td").text

			target_dict = False

			if (datum_name == "UPC"):
				target_dict = "universal_product_code"
			elif (datum_name == "Price (excl. tax)"):
				target_dict = "price_excluding_tax"
			elif (datum_name == "Price (incl. tax)"):
				target_dict = "price_including_tax"
			elif (datum_name == "Availability"):
				target_dict = "number_available"


			if target_dict:
				if "Â" in datum_value:
					datum_value = datum_value.replace("Â", "")
				if "In stock" in datum_value:
					datum_value = datum_value.replace("In stock (", "")
					datum_value = datum_value.replace(" available)", "")


			book_data[target_dict] = datum_value


	# extracting title
		book_data["title"] = soup.find("h1").text

	# extracting description product with div + id product_description
		description = soup.find("div", {"id": "product_description"})
		book_data["product_description"]=description.findNext("p").text

	# extracting category menu - ul class:breadcrumb - li before active class
		breadcrumb = soup.find("ul", {"class": "breadcrumb"})
		links = breadcrumb.select("li:not(.active)")
		book_data["category"] = links[len(links)-1].text.strip()

	# extracting image_url with div + id product_gallery
		product_gallery = soup.find("div", {"id": "product_gallery"})
		#url of the pic is extracted with the web_address + src
		book_data["image_url"] = "http://books.toscrape.com/" + \
			product_gallery.find("img")["src"]

	# extracting review_rating class star-rating Five + class icon-star
		review_rating = soup.find("p", {"class": "star-rating"})
		if review_rating.has_attr("class"): #returns True if an object has the given named attribute has_attr(object, name)
			review_rating=review_rating["class"][1]

			if review_rating == "One":
				review_rating = 1
			elif review_rating == "Two":
				review_rating = 2
			elif review_rating == "Three":
				review_rating = 3
			elif review_rating == "Four":
				review_rating = 4
			elif review_rating == "Five":
				review_rating = 5
			else:
				review_rating = 0

		else: #if the has_attr returns False, then no rating
			review_rating = 0

		book_data["review_rating"] = review_rating

	return book_data


	print(response)

category_url = "http://books.toscrape.com/catalogue/category/books/history_32/index.html"
links = find_products_url_by_category(category_url)

if links:
	books_data = []

	for url in book_data:
		books_data.append(book_data(url))

	text=""
	for char in tqdm(book_data):
		time.sleep(0.0025)
		book_data = text + char

		# creating csv file with book_data

        # Ecriture fichier csv
	with open('./scrappy_etape_2/', 'w', encoding="utf-8") as file:
            writer = csv.writer(file)

            # En têtes
            writer.writerow(books_data[0].keys())

            # Values
            writer.writerow(books_data.values())

#TEST









