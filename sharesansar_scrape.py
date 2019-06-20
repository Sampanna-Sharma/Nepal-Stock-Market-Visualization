import requests
from bs4 import BeautifulSoup

base_link = 'https://www.sharesansar.com/category/latest?page='

dates = open("dates_new.txt", 'a')
news = open('news_new.txt', 'a')

date_list = []
news_list = []

for i in range(1000,2000):		# range is changed manually 
    result = requests.get(base_link+str(i))

    c = result.content

    soup = BeautifulSoup(c, features = "html.parser")


    all_links = soup.find_all('a')

    for j in range(100,120,2):
        # print(all_links[j])
        news.write(all_links[j].h4.string+",\n")
        

    all_p = soup.find_all('p')
    for p in all_p:
        # print(p.string)
        dates.write(p.string+",\n")

# 18757 ok