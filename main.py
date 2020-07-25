from Company import *
from Scrapper import *
from  Report import *

list_of_companies = ['Airbus', 'Orange', 'Moderna', 'Fermentalg', 'Tesla', 'Total']
list_of_trends = ['up', 'up', 'up', 'down', 'down']

companies = []
for i in range(len(list_of_companies)):
    companies += [Company(company=list_of_companies[i], trend=list_of_trends[i])]

story_packs = []
# Two latest stories for each company in list of companies
for i in companies:
    scrapper = Scrapper(i)
    Story1, Story2 = scrapper.get_stories()
    story_packs += [Story1, Story2]

report = Report(companies)
report.create_report()
report.store_report()
report.store_quick_report()
report.print_report()