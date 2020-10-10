from Fast_Movers import *
from Company import *
from Scrapper import *
import pandas as pd
from datetime import datetime
import sqlite3

class Report:
    # Initializer / Instance Attributes
    def __init__(self, date):
        self.date = date
        self.connection = sqlite3.connect('Reports.db')
        self.connection.execute("CREATE TABLE IF NOT EXISTS REPORTS (Date, Sentiment, Company, Title, Content)")

    @staticmethod
    def get_company_list(language_setting='fr'):
        companies = []

        if language_setting in ['fr', 'all']:
            fast_losers = MoveFinder(url='https://fr.finance.yahoo.com/titres-pertes', trend='down')
            list_of_companies = fast_losers.get_list(language_setting=language_setting)
            for i in range(len(list_of_companies)):
                companies += [Company(company=list_of_companies[i], trend=fast_losers.trend)]
            fast_winners = MoveFinder(url='https://fr.finance.yahoo.com/titres-en-hausse', trend='up')
            list_of_companies = (fast_winners.get_list(language_setting=language_setting))
            for i in range(len(list_of_companies)):
                companies += [Company(company=list_of_companies[i], trend=fast_losers.trend)]

        if language_setting in ['en', 'all']:
            fast_winners_en = MoveFinder(url='https://finance.yahoo.com/gainers/', trend='up')
            list_of_companies = (fast_winners.get_list(language_setting=language_setting))
            for i in range(len(list_of_companies)):
                companies += [Company(company=list_of_companies[i], trend=fast_losers.trend)]

            fast_loser_en = MoveFinder(url='https://finance.yahoo.com/losers', trend='down')
            list_of_companies = (fast_winners.get_list(language_setting=language_setting))
            for i in range(len(list_of_companies)):
                companies += [Company(company=list_of_companies[i], trend=fast_losers.trend)]

        companies = [i for i in companies if i != ""]
        print(companies)
        return companies

    def create_report(self):
        companies = self.get_company_list()

        # fast_winners = MoveFinder(url='https://finance.yahoo.com/winners/', trend='up')
        # list_of_companies.append(fast_winners.get_list()[0])

        for i in companies:
            print(i.company)

        # list_of_companies = ['Airbus', 'Orange', 'Moderna', 'Fermentalg', 'Tesla']
        # list_of_trends = ['up', 'up', 'up', 'down', 'down', 'up']

        # list_of_companies = ['Total']
        # list_of_trends = ['up']

        story_packs = []
        # Two latest stories for each company in list of companies
        for i in companies:
            scrapper = Scrapper(i)
            Story1, Story2 = scrapper.get_stories()
            story_packs += [[Story1, Story2]]

        return story_packs


    def store_report(self, story_packs):
        # store in a report as a full pandas dataframe
        df = pd.DataFrame(columns=['date', 'sentiment', 'company', 'title', 'content'])
        for story_pack in story_packs:
            for story in story_pack:
                if story != 'empty':
                    report_line = {'date': story.date,
                                   'sentiment': story.sentiment,
                                   'company': story.company,
                                   'title': story.title,
                                   'content': story.content}
                    df = df.append(report_line, ignore_index=True)

        #Store new lines into pyodbc sqlite db
        cursor = self.connection.cursor()
        #df.to_sql(sql_command, connection)

        #Also store as CSV
        path = 'Reports\\full_report.csv'
        old_path = f'Reports\\full_report_archive_{str(datetime.today().datetime())}.csv'
        try:
            full_report = pd.read_csv(path)
            full_report.to_csv(old_path, sep=';', decimal=',', encoding='utf-8')
            full_report = full_report.append(df)
            full_report = full_report.drop_duplicates()
            full_report.to_csv(path, sep=';', decimal=',', encoding='utf-8')
        except:
            # FIX BARE EXCEPT CLAUSE
            print('CREATING NEW REPORT')
            full_report = df
            full_report.to_csv(path, sep=';', decimal=',', encoding='utf-8')


    @staticmethod
    def print_quick_report():
        """
        This function prints a summary of the latest report
        :return:
        """
        print('function not yet written')
        # print a summary of the report as a structured pandas dataframe
        #Summary will include only date title and sentiment

    @staticmethod
    def store_quick_report():
        print('function not yet written')
        # store the quick report for later viewing
        # Will be stored both in csv and in SQL database