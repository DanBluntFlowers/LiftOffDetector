# importing the necessary packages
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import html
from datetime import datetime
from Stories import *

options = Options()
options.add_argument("--headless")
options.add_argument("--incognito")
options.add_argument("--log-level=3")
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
        driver.set_page_load_timeout(120)
        zb_url = 'https://www.zonebourse.com'
        company = self.company.company
        print(company)

        link1 = company_url(company)

        print('--FINDING COMPANY')
        print(link1)
        xpath_company = '//*[@id="ALNI0"]/tbody/tr[2]/td[3]'
        # try
        driver.get(link1)
        try:
            href = driver.find_element_by_xpath(xpath_company).get_attribute('innerHTML')
            href = href.split(' ')[1].split('href=')[-1].split('"')[1]
            link2 = zb_url + href + '/actualite/'
        except:
            pass


        print('--FINDING NEWS RELATED TO COMPANY')
        xpath_box = '//*[@id="autocomplete_forum"]'
        try:
            print(link2)
            driver.get(link2)
            searchbox = driver.find_element_by_xpath(xpath_box)
            searchbox.send_keys(company)
            searchbox.send_keys(Keys.ENTER)
            time.sleep(.3)
        except:
            print('--NEWS NOT FOUND')
            return 'empty', 'empty'
        try:
            method = 'method_1'
            article_links = ['//*[@id="ALNI0"]/tbody/tr[{}]/td'.format(i) for i in range(1, 3)]
            article_links = [
                driver.find_element_by_xpath(i).get_attribute('innerHTML').split('href=')[-1].split('><')[0].split('"')[1]
                for i in article_links
            ]
            article_times = ['//*[@id="ALNI0"]/tbody/tr[{}]/td/a/div[2]'.format(i) for i in range(1, 3)]
            article_times = [driver.find_element_by_xpath(i).get_attribute('innerHTML') for i in article_times]
            print('METHOD_1 WORKING')

        except:
            # if error go through possible links and check bold area
            print('MOVING ON TO METHOD 2')
            method = 'method_2'
            article_times = []
            driver.get(link2)
            article_links = []
            for i in range(1, 3):
                xpath_news = f'//*[@id="ALNI4"]/tbody/tr[{i}]/td[2]/a'
                try:
                    news_link = driver.find_element_by_xpath(xpath_news)
                    article_links.append(news_link.get_attribute('href'))
                except:
                    print('-- Method_2 also failed, moving on')

        article_contents = []
        for j in range(len(article_links)):
            if method == 'method_1':
                link3 = zb_url + article_links[j]
            elif method == 'method_2':
                link3 = article_links[j]
            print(f'--FINDING ARTICLE {j + 1}')
            try:
                driver.set_page_load_timeout(4.3)
                driver.save_screenshot("bye" + str(link3) + ".png")
                driver.get(link3)
                driver.set_page_load_timeout(120)
                print("DID NOT STOP LOAD !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            except:
                print("STOPPED LOAD !!!!!!!!!!!!!!!!!!!!!!")
                driver.set_page_load_timeout(120)
                pass
            try:
                article_contents_temp = driver.find_elements_by_xpath("//div[contains(@id, 'grantexto')]")
                article_contents_temp = [''.join([i.text for i in article_contents_temp if type(i) != str])]
                article_contents += article_contents_temp
                print(f'TESTTESTESTETSTEST  Article Temp Contents: {article_contents_temp}')

                try:
                    date = driver.find_element_by_xpath(
                        '//*[@id="zbCenter"]/div/table[2]/tbody/tr[3]/td[1]/div[2]/div[1]/div[2]'
                    )
                    date = date.text
                except:
                    try:
                        date = driver.find_element_by_xpath(
                            '//*[@id="zbCenter"]/div/span/table[4]/tbody/tr/td[1]/div[3]/div[1]/div[2]'
                        )
                        date = date.text
                    except:
                        print('not_finding_date')
                        date = 'unknown'
                        pass
                #setup different date formats ?

                print(f'date is as follows: {date}')
                try:
                    date = datetime.strptime(date, '%d/%m/%Y | %H:%M')
                except:
                    print('date unsupported format')

                article_times += [str(date)]

                print('--CONTENTS LOADED')

            except Exception as e:
                print(e, 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAARRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRG')
                print('CONTENTS NULL')
                article_contents += ['Empty']
                continue

        print('contents done ! ---> Moving on to sentiment analysis')

        sentiment = []
        for p in range(len(article_contents)):
            contents_txt = html.unescape(article_contents[p])
            contents_english = translator.translate(contents_txt).text
            score = analyser.polarity_scores(contents_english)
            sentiment += [str(score['compound']) + ' vs ' + str(self.company.trend)]

        article_contents = [i if i != '' else 'empty' for i in article_contents]

        if len(article_contents) > 0 and len(article_times) > 0 and len(article_contents) > 0:
            story1 = Story(date=article_times[0], sentiment=sentiment[0], company=company,
                           title='to_be_done', content=article_contents[0])
        else:
            story1 = 'empty'
        if len(article_contents) > 1 and len(article_times) > 1 and len(article_contents) > 1:
            # take stories less than 24hrs old
            story2 = Story(date=article_times[1], sentiment=sentiment[1], company=company,
                           title='to_be_done', content=article_contents[1])
        else:
            story2 = 'empty'
        return story1, story2

        # dataframe_company = pd.DataFrame(company_list)
        # dataframe_company['Article Times'] = article_times
        # dataframe_company['Article Contents'] = article_contents

        # find stories of a given company
        # check match in terms of date & sentiment
        # initialise story objects
        # output all stories for a given company that match in terms of time

