from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import time
from .models import BusiModel,ScrapedData


def UpdateReviews():
    businesses = BusiModel.objects.all()
    for busi in businesses:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1200x600')
        browser = webdriver.Chrome()
        browser2 = webdriver.Chrome()
        browser.get(busi.Google_URL)
        browser2.get(busi.Zomato_URL)

        time.sleep(2)
        browser.find_element_by_class_name("section-reviewchart-numreviews").click()
        elem2 = browser2.find_element_by_xpath("//*[@id='selectors']")
        elem2.find_element_by_xpath(".//a[@data-sort='reviews-dd']").click()
        time.sleep(2)
        elem = browser.find_element_by_xpath("//div[@class='section-listbox section-scrollbox scrollable-y scrollable-show']")

        scrollable = elem.find_element_by_xpath(".//div[@class='section-loading noprint']")

        # while scrollable:
        #     try:
        browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',elem)
        time.sleep(2)
        scrollable = elem.find_element_by_xpath(".//div[@class='section-loading noprint']")
            # except NoSuchElementException as exception:
            #     break

        # while True:
        #     try:
        browser.find_element_by_class_name("zs-load-more-count").click()
        time.sleep(2)
            # except NoSuchElementException as exception:
            #     break

        soup = BeautifulSoup(browser.page_source, 'lxml')
        browser.close()

        soup2 = BeautifulSoup(browser2.page_source, 'lxml')
        browser2.close()

        users2 = []
        users2 = soup.find_all('div', {'class': 'ui segment clearfix brtop '})
        users2.append(soup.find('div', {'class': 'ui segment clearfix br0 '}))
        Users = soup.find_all('div', {'jstcache': '1031'})

        reviews = ScrapedData.objects.filter(Bus=busi.id)
        for user in range(len(Users)):
            id = Users[user].find('a',{'jstcache':'1033'})['href'].split("/")[5]
            for rev in reviews:
                if rev.Id == id:
                    continue
                else:
                    inst = ScrapedData()
                    inst.Name = Users[user].find('div', {'jstcache': '1034'}).get_text().strip()
                    inst.Id = id
                    inst.Bus = BusiModel.objects.get(id=busi.id)
                    inst.Username = busi.Username
                    inst.Review = Users[user].find('span', {'jstcache': '1053'}).get_text().strip()
                    inst.Date = Users[user].find('span', {'jstcache': '1051'}).get_text().strip()
                    inst.Rating = Users[user].find('span', {'class': 'section-review-stars'})['aria-label']
                    inst.save()

        for user in range(len(users2)):
            divtag = users2[user].find(class_='header nowrap ui left')
            id = divtag.find('a')['data-entity_id']
            for rev in reviews:
                if rev.Id == id:
                    continue
                else:
                    inst = ScrapedData()
                    inst.Name = divtag.get_text().strip()
                    inst.Id = id
                    try:
                        divs = users2[user].find(class_="rev-text mbot0 ")
                        inst.Review = divs.get_text().strip()
                        inst.Rating = divs.find('div')['aria-label']
                    except AttributeError:
                        divs2 = users2[user].find(class_="rev-text mbot0 hidden ")
                        inst.Review = divs2.get_text().strip()
                        inst.Rating = divs2.find('div')['aria-label']
                    inst.Date = users2[user].find('div', {'class': 'fs12px pbot0 clearfix'}).get_text()
                    inst.save()

