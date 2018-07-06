from bs4 import BeautifulSoup

file = open('zomato.txt','r',encoding='utf-8')
soup = file.read()
file.close()

souping = BeautifulSoup(soup,'lxml')

Users = []

Users = souping.find_all('div',{'class':'ui segment clearfix brtop '})
Users.append(souping.find('div',{'class':'ui segment clearfix br0 '}))


for i in range(len(Users)):
    divtag = Users[i].find(class_='header nowrap ui left')
    name = divtag.get_text().strip()
    id = divtag.find('a')['data-entity_id']
    try:
        divs = Users[i].find(class_="rev-text mbot0 ")
        review = divs.get_text().strip()
        rating = divs.find('div')['aria-label']
    except AttributeError:
        divs2 = Users[i].find(class_="rev-text mbot0 hidden ")
        review = divs2.get_text().strip()
        rating = divs2.find('div')['aria-label']
    date = Users[i].find('div',{'class':'fs12px pbot0 clearfix'}).get_text()
    print(name,id,review,rating,date)

