import requests
from bs4 import BeautifulSoup

for i in range(500):
    page = requests.get('http://www.tate.org.uk/art/search?page='+str(i))
    html_doc = page.content
    soup = BeautifulSoup(html_doc, 'html.parser')
    divs = soup.find_all(class_='grid-item-image')
    for div in divs:
        url = 'http://www.tate.org.uk' + div.find('a')['href']
        print url
