import pandas as pd
from datetime import datetime

class Signal():
    def __init__(self):
        self.report = pd.read_csv("dags/Reports/full_report.csv", sep=";", decimal=",")
        self.now = datetime.now()

    def get_signals(self):
        report_curated_negative = self.report[(self.report['sentiment'].str.contains('-')) &
                                              (self.report['sentiment'].str.contains('down'))]
        print(type(report_curated_negative))
        report_curated_negative['strength'] = report_curated_negative.apply(
            lambda x: float(x['sentiment'].split('vs')[0]), axis=1
        )
        report_curated_negative = report_curated_negative[report_curated_negative['strength'] < -0.8]


        report_curated_positive = self.report[(~self.report['sentiment'].str.contains('-')) &
                                              (self.report['sentiment'].str.contains('up'))]
        report_curated_positive['strength'] = report_curated_positive.apply(
            lambda x: float(x.sentiment.split('vs')[0]), axis=1
        )
        report_curated_positive = report_curated_positive[report_curated_positive['strength'] > 0.8]
        #report_curated_positive = report_curated_positive[report_curated_positive.date ]

        # ensure timedelta is less than 20 hours 


        return report_curated_positive, report_curated_negative