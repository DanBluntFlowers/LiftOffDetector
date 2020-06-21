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


class Scrapper:
    # Initializer / Instance Attributes
    def __init__(self, company):
        self.company = company

    def get_stories(self):
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        url_prefix = 'https://www.zonebourse.com/recherche/actualites/?aComposeInputSearch=s_'
        zb_prefix = 'https://www.zonebourse.com'

        company_url = url_prefix + company_name
        print(company_url)
        r1 = requests.get(company_url)
        coverpage = r1.content
        soup1 = BeautifulSoup(coverpage, 'html5lib')
        coverpage_news = soup1.find(class_='tabBody')
        stories = str(coverpage_news).split('</tr>')
        stories = stories[:-1]
        links = [i.split('href="')[-1].split('" style')[0] for i in stories]
        print(links)
        for i in stories:
            timestamps += [i.split("""color:#818181;">""")[-1].split('</div>')[0]]
        timestamps = [datetime.strptime(i, "%Y-%m-%d %H:%M:%S") for i in timestamps]
        now = datetime.now()
        now_string = now.strftime("%Y-%m-%d %H:%M:%S")
        now_string = datetime.strptime(now_string, "%Y-%m-%d %H:%M:%S")
        validated_times = [i for i in range(len(timestamps)) if (now_string - timestamps[i]).days == 1]

        titles = []
        validated_timestamps = [timestamps[i] for i in validated_times]

        for i in validated_times:
            url = zb_prefix + links[i]
            print(url)
            driver.get(url)
            story = driver.find_element_by_xpath(
                """/html/body/div[6]/table/tbody/tr/td[1]/table/tbody/tr[2]/td/div/table[2]/tbody/tr[3]/td[1]/div[2]/div/span/div[1]""").text
            all_stories += [story]


        #find stories of a given company
        #check match in terms of date & sentiment
        #initialise story objects
        #output all stories for a given company that match in terms of time


        url_prefix = 'https://www.zonebourse.com/recherche/actualites/?aComposeInputSearch=s_'
        zb_prefix = 'https://www.zonebourse.com'