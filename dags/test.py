from Company import *
from Scrapper import *
from Report import *
from Fast_Movers import *

companies = []

fast_losers = MoveFinder(url='https://fr.finance.yahoo.com/titres-pertes', trend='down')
#fast_losers = MoveFinder(url='https://finance.yahoo.com/gainers/', trend='down')

list_of_companies = (fast_losers.get_list())
for i in range(len(list_of_companies)):
    companies += [Company(company=list_of_companies[i], trend=fast_losers.trend)]

print(list_of_companies)