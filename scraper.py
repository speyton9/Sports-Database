from datetime import datetime, timedelta


class Scraper:
    def __init__(self, to=25):
        self.__to = to

    def time(self):
        return self.__to

# Allows user to search for range of days
def date_range(range_days):
    dRange = range_days[0].split(':')
    # Calculates number of days in range
    diff = str(datetime.strptime(dRange[1], "%Y-%m-%d") - datetime.strptime(dRange[0], "%Y-%m-%d")).split(' ')
    dr = []
    # Adds each day in range to list dr to be used for getting data from online
    i = 0
    while i < int(diff[0]) + 1:
        x = str(datetime.strptime(dRange[0], "%Y-%m-%d") + timedelta(days=i))
        dr.append(x[:10])
        i += 1
    return dr
