from bs4 import BeautifulSoup

with open('home.html', 'r')  as html_file:
    content=html_file.read()
    soup = BeautifulSoup(content, 'html.parser')
    # tags = soup.find('h5') #finds the first occurence of h5 tag and stops
    tags = soup.find_all('h5')
print(tags)
