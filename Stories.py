class Story:
    # Initializer / Instance Attributes
    def __init__(self, date, sentiment, match, company, title):
        self.date = date
        self.sentiment = sentiment
        self.match = match
        self.company = company
        self.title = title
        self.content

    #Instance method
    def verify_match(self, Company, Date, Sentiment):
