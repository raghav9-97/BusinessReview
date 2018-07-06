from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time


browser = webdriver.Chrome()
browser = webdriver.Firefox(firefox_options=options,capabilities=DesiredCapabilities.FIREFOX)
browser.get("https://www.zomato.com/hyderabad/mcdonalds-hitech-city/reviews")

time.sleep(2)

elem = browser.find_element_by_id("selectors")
elem.find_element_by_xpath(".//a[@data-sort='reviews-dd']").click()
time.sleep(2)

while True:
    try:
        browser.find_element_by_class_name("zs-load-more-count").click()
        time.sleep(2)
    except NoSuchElementException as exception:
        break

soup = BeautifulSoup(browser.page_source,'lxml')
browser.close()

with open('zomato.txt','w',encoding='utf-8') as file:
    file.write(soup.prettify())
