from selenium import webdriver
from bs4 import BeautifulSoup
from .models import BusiModel
from signup.models import UserDefined
from textblob import TextBlob
import smtplib
import datetime
from selenium.common.exceptions import NoSuchElementException
import time
from .models import ScrapedData
from BusinessReview.celery import app

@app.task
def scrapegoogle(url,uid,id):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1200x600')
    browser = webdriver.Chrome()
    browser.get(url)

    time.sleep(2)
    browser.find_element_by_xpath("//button[@class='section-reviewchart-numreviews']").click()
    time.sleep(2)
    elem = browser.find_element_by_xpath("//div[@class='section-listbox section-scrollbox scrollable-y scrollable-show']")

    scrollable = elem.find_element_by_xpath(".//div[@class='section-loading noprint']")

    while scrollable:
        try:
            browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',elem)
            time.sleep(2)
            scrollable = elem.find_element_by_xpath(".//div[@class='section-loading noprint']")
        except NoSuchElementException as exception:
            break

    soup = BeautifulSoup(browser.page_source,'lxml')
    browser.close()

    Users = soup.find_all('div',{'class':'section-review-line section-review-line-with-indent section-review-line-with-indented-border'})
    with open('google.txt','w',encoding='utf8') as file:
        file.write(str(Users))

    for i in range(len(Users)):
        inst = ScrapedData()
        inst.Name = Users[i].find('div', {'class': 'section-review-title'}).get_text().strip()
        idhead = Users[i].find('div',{'class': 'section-review-titles section-review-titles-with-menu'})
        inst.Id = idhead.find('a')['href'].split("/")[5]
        inst.User = uid
        inst.Bus = BusiModel.objects.get(id=id)
        Review = Users[i].find('span', {'class':'section-review-text'}).get_text().strip()
        inst.Review = Review
        inst.Polarity = TextBlob(Review).sentiment.polarity
        inst.Date = Users[i].find('span', {'class':'section-review-publish-date'}).get_text().strip()
        inst.Rating = Users[i].find('span', {'class': 'section-review-stars'})['aria-label']
        inst.save()

@app.task
def scrapezomato(url,uid,id):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1200x600')
    browser = webdriver.Chrome()
    browser.get(url)

    time.sleep(2)
    elem = browser.find_element_by_xpath("//*[@id='selectors']")
    elem.find_element_by_xpath(".//a[@data-sort='reviews-dd']").click()
    time.sleep(2)

    while True:
        try:
            browser.find_element_by_class_name("zs-load-more-count").click()
            time.sleep(2)
        except NoSuchElementException as exception:
            break

    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.close()
    Users = []

    Users = soup.find_all('div', {'class': 'ui segment clearfix brtop '})
    Users.append(soup.find('div', {'class': 'ui segment clearfix br0 '}))
    for i in range(len(Users)):
        inst = ScrapedData()
        divtag = Users[i].find(class_='header nowrap ui left')
        inst.Name = divtag.get_text().strip()
        inst.Id = divtag.find('a')['data-entity_id']
        inst.User = uid
        inst.Bus = BusiModel.objects.get(id=id)
        try:
            divs = Users[i].find(class_="rev-text mbot0 ")
            Review = divs.get_text().strip()
            inst.Review = Review
            inst.Polarity = TextBlob(Review).sentiment.polarity
            inst.Rating = divs.find('div')['aria-label']
        except AttributeError:
            divs2 = Users[i].find(class_="rev-text mbot0 hidden ")
            Review = divs2.get_text().strip()
            inst.Review = Review
            inst.Polarity = TextBlob(Review).sentiment.polarity
            inst.Rating = divs2.find('div')['aria-label']
        inst.Date = Users[i].find('div', {'class': 'fs12px pbot0 clearfix'}).get_text()
        inst.save()

@app.task
def UpdateReviews():
    businesses = BusiModel.objects.all()
    for busi in businesses:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1200x600')
        browser = webdriver.Chrome()
        browser.get(busi.Google_URL)

        time.sleep(2)
        browser.find_element_by_xpath("//button[@class='section-reviewchart-numreviews']").click()
        time.sleep(2)
        elem = browser.find_element_by_xpath("//div[@class='section-listbox section-scrollbox scrollable-y scrollable-show']")

        browser2 = webdriver.Chrome()
        browser2.get(busi.Zomato_URL)

        time.sleep(2)
        elem2 = browser2.find_element_by_xpath("//*[@id='selectors']")
        elem2.find_element_by_xpath(".//a[@data-sort='reviews-dd']").click()
        time.sleep(2)

        scrollable = elem.find_element_by_xpath(".//div[@class='section-loading noprint']")

        while scrollable:
            try:
                browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',elem)
                time.sleep(2)
                scrollable = elem.find_element_by_xpath(".//div[@class='section-loading noprint']")
            except NoSuchElementException as exception:
                break

        while True:
            try:
                browser2.find_element_by_class_name("zs-load-more-count").click()
                time.sleep(2)
            except NoSuchElementException as exception:
                break

        soup = BeautifulSoup(browser.page_source, 'lxml')
        browser.close()
        Users = soup.find_all('div', {'class': 'section-review-line section-review-line-with-indent section-review-line-with-indented-border'})

        soup2 = BeautifulSoup(browser2.page_source, 'lxml')
        browser2.close()

        users2 = soup2.find_all('div', {'class': 'ui segment clearfix brtop '})
        users2.append(soup2.find('div', {'class': 'ui segment clearfix br0 '}))

        reviews = ScrapedData.objects.filter(Bus=busi.id).values_list('Id', flat=True)
        for user in range(len(Users)):
            idhead = Users[user].find('div', {'class': 'section-review-titles section-review-titles-with-menu'})
            id = idhead.find('a')['href'].split("/")[5]
            if id in reviews:
                continue
            else:
                inst = ScrapedData()
                inst.Name = Users[user].find('div', {'class': 'section-review-title'}).get_text().strip()
                inst.Id = id
                inst.Bus = BusiModel.objects.get(id=busi.id)
                inst.User = busi.User_id
                Review = Users[user].find('span', {'class': 'section-review-text'}).get_text().strip()
                inst.Review = Review
                inst.Polarity = TextBlob(Review).sentiment.polarity
                inst.Date = Users[user].find('span', {'class': 'section-review-publish-date'}).get_text().strip()
                inst.Rating = Users[user].find('span', {'class': 'section-review-stars'})['aria-label']
                inst.save()

        for user in range(len(users2)):
            divtag = users2[user].find(class_='header nowrap ui left')
            id = divtag.find('a')['data-entity_id']
            if id in reviews:
                continue
            else:
                inst = ScrapedData()
                inst.Name = divtag.get_text().strip()
                inst.Id = id
                inst.Bus = BusiModel.objects.get(id=busi.id)
                inst.User = busi.User_id
                try:
                    divs = users2[user].find(class_="rev-text mbot0 ")
                    Review = divs.get_text().strip()
                    inst.Review = Review
                    inst.Polarity = TextBlob(Review).sentiment.polarity
                    inst.Rating = divs.find('div')['aria-label']
                except AttributeError:
                    divs2 = users2[user].find(class_="rev-text mbot0 hidden ")
                    Review = divs2.get_text().strip()
                    inst.Review = Review
                    inst.Polarity = TextBlob(Review).sentiment.polarity
                    inst.Rating = divs2.find('div')['aria-label']
                inst.Date = users2[user].find('div', {'class': 'fs12px pbot0 clearfix'}).get_text()
                inst.save()

@app.task
def sendmail():
    users = UserDefined.objects.all()
    for i in users:
        businesses = BusiModel.objects.filter(User_id=i.id)
        for bus in businesses:
            target = i.email
            count = 0
            if bus.Manager_id:
                target = UserDefined.objects.filter(id=bus.Manager_id).values_list('email',flat=True)
            busrev = ScrapedData.objects.filter(Bus_id=bus.id)
            for rev in busrev:
                if rev.TimeStamp == bus.TimeStamp:
                    continue
                elif rev.TimeStamp == datetime.date.today():
                    count = count + 1
                else:
                    continue
            if count != 0:
                msg = "You have %s new reviews today for %s %s" % (count,bus.Business,bus.Address)

                if target == i.email:
                    msg = msg + "\nYou are receiving this mail as you have not set up any manager for this location"

                gmail_username = "raghu2288661"
                gmail_pass = "#shinTY@97"

                server = smtplib.SMTP_SSL('smtp.gmail.com',465)
                server.login(gmail_username,gmail_pass)

                server.sendmail('raghu2288661@gmail.com',target,msg)

                server.close()
