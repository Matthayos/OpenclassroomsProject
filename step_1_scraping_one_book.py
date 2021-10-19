# Extracting following data:

# product_page_url
# universal_product_code (upc)
# price_excluding_tax
# price_including_tax
# number_available
# title
# product_description
# category
# image_url

# review_rating


# writing down infos in a .csv

import requests
from bs4 import BeautifulSoup
import csv


book_data = {"product_page_url": "http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"}

response = requests.get(book_data["product_page_url"])

if response.ok:
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
#print(book_data)
#print(response)
#print(data)

		if target_dict:
			if "Â" in datum_value:
				datum_value = datum_value.replace("Â", "")


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

# creating csv file with book_data
#codec "charmap" unicodeEncoreError. Had to write -> with open("./scrappy_etape_1.csv", "w", encoding="utf-8") as file:


with open("./step_1_scraping_one_book.csv", "w", encoding="utf-8") as file:
	writer = csv.writer(file, delimiter=",")

# headers
	writer.writerow(book_data.keys())
# values
	writer.writerow(book_data.values())

with open("step_1_scraping_one_book.csv", "r") as csv_file:
	csv_reader = csv.reader(csv_file)

	#print(csv_reader)


#print(book_data)







