from googletrans import Translator

# inspired by https://hackernoon.com/scraping-yahoo-finance-data-using-python-ayu3zyl

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import os


class MoveFinder:

    def __init__(self, url, trend):
        self.url = url
        self.trend = trend
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--incognito")
        options.add_argument("--log-level=3")
        options.add_argument("window-size=1920,1080")
        self.driver_1 = webdriver.Chrome(options=options)

    def get_list(self, language_setting='fr', double_click=False):
        self.driver_1.get(self.url)
        print(self.url)
        time.sleep(3)  #
        #self.driver_1.find_element_by_xpath('//*[@id="scroll-down-btn"]').click() #ony necessary outside of headless
        time.sleep(4)  #


        self.driver_1.find_element_by_xpath('//*[@id="consent-page"]/div/div/div/div[2]/div[2]/form/button').click()
        time.sleep(3)
        try:
            self.driver_1.find_element_by_xpath('//*[@id="scr-res-table"]/div[1]/table/thead/tr/th[6]/span').click()
            if double_click is True:
                self.driver_1.find_element_by_xpath('//*[@id="scr-res-table"]/div[1]/table/thead/tr/th[6]/span').click()
        except:
            self.driver_1.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            self.driver_1.find_element_by_xpath('//*[@id="scr-res-table"]/div[1]/table/thead/tr/th[6]/span').click()
            if double_click is True:
                self.driver_1.find_element_by_xpath('//*[@id="scr-res-table"]/div[1]/table/thead/tr/th[6]/span').click()

        time.sleep(4)
        print('PRINTING SCREENSHOT')
        print(os.getcwd())
        self.driver_1.save_screenshot("hello_" + str(self.url) + ".png")
        data = self.driver_1.page_source
        soup = BeautifulSoup(data)

        names = []
        # for listing in soup.find_all('tr', attrs={'class': 'simpTblRow'}):
        #     for name in listing.find_all('td'):
        #         print('####################', listing, '#################')
        #         print(name)

        if language_setting == 'en':
            for listing in soup.find_all('tr', attrs={'class': 'simpTblRow'}):
                for name in listing.find_all('td', attrs={'aria-label': 'Name'}):
                    names.append(name.text)

        if language_setting == 'fr':
            for listing in soup.find_all('tr', attrs={'class': 'simpTblRow'}):
                for name in listing.find_all('td', attrs={'aria-label': 'Nom'}):
                    names.append(name.text)

        names = [i.replace('SA', '').replace('S.A.', '') for i in names if i != ""]
        return names

