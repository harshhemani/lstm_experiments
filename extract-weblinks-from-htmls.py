from bs4 import BeautifulSoup as bs

for i in range(1, 1001):
    soup = bs(open("htmls/top-"+str(i)+"000-sites"))
    table = soup.find('table', attrs={'class':'bordered-table zebra-striped'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        col_num = cols[0].text.strip()
        link = cols[1].find('a').text.strip()
        print link
        
