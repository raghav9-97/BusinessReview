from selenium import webdriver
from bs4 import BeautifulSoup
import time

def scrapegoogle(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1200x600')
    browser = webdriver.Chrome()
    browser.get(url)

    time.sleep(2)
    browser.find_element_by_class_name("section-reviewchart-numreviews").click()
    time.sleep(2)
    elem = browser.find_element_by_xpath("//div[@class='section-listbox section-scrollbox scrollable-y scrollable-show']")

    scrollable = elem.find_element_by_xpath(".//div[@class='section-loading noprint']")


    while scrollable == 'section-loading noprint':

        browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',elem)
        scrollable = elem.find_element_by_xpath(".//div[@jstcache='1117']").get_attribute('class')

    soup = BeautifulSoup(browser.page_source,'lxml')
    browser.close()

    Users = soup.find_all('div', {'jstcache': '1031'})
    print(Users)


scrapegoogle("https://www.google.com/maps/place/McDonald's/@17.4345328,78.3864507,15z/data=!4m5!3m4!1s0x0:0xdfe4737112cb9bc0!8m2!3d17.4345328!4d78.3864507")

    # for i in range(len(Users)):
    #     name = Users[i].find('div', {'jstcache': '1034'}).get_text().strip()
    #     review = Users[i].find('span', {'jstcache': '1053'}).get_text().strip()
    #     date = Users[i].find('span', {'jstcache': '1051'}).get_text().strip()
    #     rating = Users[i].find('span', {'class': 'section-review-stars'})['aria-label']
    #     print(name,review,rating,date)

