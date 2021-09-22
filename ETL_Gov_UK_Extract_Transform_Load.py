import requests
from bs4 import BeautifulSoup
import csv

# lien de la page à scrapper
url = "https://www.gov.uk/search/news-and-communications"
reponse = requests.get(url)
page = reponse.content
print(page)

soup = BeautifulSoup(page, "html.parser")

#récupération de tous les titres LINK n'existe plus, donc remplacé par -title
titres = soup.find_all("a", class_="gem-c-document-list__item-title")
titre_textes = []
for titre in titres:
	titre_textes.append(titre.string)

descriptions = soup.find_all("p", class_="gem-c-document-list__item-description")
description_textes = []
for description in descriptions:
	description_textes.append(description.string)

# création du fichier data.csv
en_tete = ['titre', 'description']
with open('data.csv', 'w') as fichier_csv:
	writer = csv.writer(fichier_csv, delimiter=',')
	writer.writerow(en_tete)
	# zip permet d'itérer sur deux listes à la fois
	for titre, description in zip(titre_textes, description_textes):
		writer.writerow([titre, description])

