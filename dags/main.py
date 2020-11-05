from Report import *

today = date.today()


report = Report(today)
story_packs = report.create_report()
report.store_report(story_packs)
report.store_quick_report()
report.print_quick_report()

driver.close()
