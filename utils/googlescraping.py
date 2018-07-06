from bs4 import BeautifulSoup

file = open('google.txt','r',encoding='utf-8')
soup = file.read()
file.close()

souping = BeautifulSoup(soup,'lxml')
Users = souping.find_all('div',{'jstcache':'1031'})

data = {}
for i in range(len(Users)):
    name = Users[i].find('div',{'jstcache':'1034'}).get_text().strip()
    review = Users[i].find('span',{'jstcache':'1053'}).get_text().strip()
    date = Users[i].find('span',{'jstcache':'1051'}).get_text().strip()
    rating = Users[i].find('span',{'class':'section-review-stars'})['aria-label']
    data[name] = [rating,date,review]

print(data)