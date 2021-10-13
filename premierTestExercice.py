from bs4 import BeautifulSoup
 
html = """
    <html>
    <table class="table table-striped">
        <tbody>
        <tr>
            <th>UPC</th><td>4165285e1663650f</td>
        </tr>
        <tr>
            <th>Product Type</th><td>Books</td>
        </tr>
            <tr>
                <th>Price (excl. tax)</th><td>£54.23</td>
            </tr>
                <tr>
                    <th>Price (incl. tax)</th><td>£54.23</td>
                </tr>
                <tr>
                    <th>Tax</th><td>£0.00</td>
                </tr>
            <tr>
                <th>Availability</th>
                <td>In stock (20 available)</td>
            </tr>
            <tr>
                <th>Number of reviews</th>
                <td>0</td>
            </tr>
        </tbody>
    </table>
     </html>
 """

soup = BeautifulSoup(html,"html.parser")
tables = soup.findChildren('table')

# This will get the first (and only) table. Your page may have more.
my_table = tables[0]

# You can find children with multiple tags by passing a list of strings
rows = my_table.findChildren(['tr'])

print("Product Information")

for row in rows:
    infos = row.findChildren('th')
    values = row.findChildren('td')
    for info in infos:
        desc = info.string
    for value in values:
        valeur = value.string
    
    print("The" + " " + desc + " " + "is" + " " + valeur)
	



