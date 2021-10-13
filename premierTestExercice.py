import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html'

response = requests.get(url)

if response.ok:
	soup = BeautifulSoup (response.text,"html.parser")
	title = soup.find('title')
	table = soup.find('table')
	


print(table.text)
print(title.text)

	



