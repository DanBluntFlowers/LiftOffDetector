# importing the necessary packages
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import html
import pandas as pd
from Stories import *

options = Options()
options.add_argument("--headless")
options.add_argument("--incognito")
driver = webdriver.Chrome(options=options)
translator = Translator()
analyser = SentimentIntensityAnalyzer()


def company_url(company):
    company_url = "https://www.zonebourse.com/recherche/?mots={}&RewriteLast=recherche&noredirect=1&type_recherche=0".format(
        company)
    return company_url


class Scrapper:
    # Initializer / Instance Attributes
    def __init__(self, company):
        self.company = company

    def get_stories(self):
        zb_url = 'https://www.zonebourse.com'
        company = self.company
        # company_list = [company for i in range(2)]
        link1 = company_url(company)
        xpath_company = '//*[@id="ALNI0"]/tbody/tr[2]/td[3]'
        driver.get(link1)
        href = driver.find_element_by_xpath(xpath_company).get_attribute('innerHTML')
        href = href.split(' ')[1].split('href=')[-1].split('"')[1]
        link2 = zb_url + href + '/actualite/'
        driver.get(link2)
        xpath_box = '//*[@id="autocomplete_forum"]'
        searchbox = driver.find_element_by_xpath(xpath_box)
        searchbox.send_keys(company)
        searchbox.send_keys(Keys.ENTER)
        time.sleep(.3)
        article_links = ['//*[@id="ALNI0"]/tbody/tr[{}]/td'.format(i) for i in range(1, 3)]
        article_links = [
            driver.find_element_by_xpath(i).get_attribute('innerHTML').split('href=')[-1].split('><')[0].split('"')[1]
            for i in article_links]
        article_times = ['//*[@id="ALNI0"]/tbody/tr[{}]/td/a/div[2]'.format(i) for i in range(1, 3)]
        article_times = [driver.find_element_by_xpath(i).get_attribute('innerHTML') for i in article_times]

        article_contents = []
        for j in range(len(article_links)):
            link3 = zb_url + article_links[j]
            driver.get(link3)
            try:
                article_contents += [
                    driver.find_element_by_xpath('//*[@id="grantexto"]').get_attribute('innerHTML').split('<br>')[0]]
            except:
                article_contents += ['Empty']
                continue

        sentiment = []
        for p in range(len(article_contents)):
            contents_txt = html.unescape(article_contents[p])
            contents_english = translator.translate(contents_txt).text
            score = analyser.polarity_scores(contents_english)
            sentiment += [score['compound']]


        story1 = Story(date=article_times[0], sentiment=sentiment[0], company=company,
                       title='to_be_done', content=article_contents[0])

        story2 = Story(date=article_times[1], sentiment=sentiment[1], company=company,
                       title='to_be_done', content=article_contents[1])

        # dataframe_company = pd.DataFrame(company_list)
        # dataframe_company['Article Times'] = article_times
        # dataframe_company['Article Contents'] = article_contents

        return story1, story2

        # find stories of a given company
        # check match in terms of date & sentiment
        # initialise story objects
        # output all stories for a given company that match in terms of time


