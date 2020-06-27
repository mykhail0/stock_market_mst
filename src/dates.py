import sys

def make_date_readable(date):
    return date[0:4]+"."+date[4:6]+"."+date[6:]

def make_dateInterval_readable(date):
    (start, end) = date
    return make_date_readable(start)+"-"+make_date_readable(end)

def make_dates_readable(dates):
    readable = []
    for date in dates:
        readable.append(make_dateInterval_readable(date))
    return readable



def increment_year(date):
    new_year = int(date[0:4]) + 1
    return str(new_year)+date[4:]

def increment_month(date):
    new_month = int(date[4:6]) + 1
    if new_month == 13:
        new_month = 1
        date = increment_year(date)

    new_month = str(new_month)
    if int(new_month) < 10:
        new_month = "0"+new_month

    return date[0:4]+new_month+date[6:]



#1 jesli x później niż y, -1 jeśli odwrotnie, 0 jeśli to samo
def cmp_dates(x, y):
    if x == y:
        return 0
    if int(x[0:4]) > int(y[0:4]):
        return 1
    if int(x[0:4]) < int(y[0:4]):
        return - 1
    if int(x[4:6]) > int(y[4:6]):
        return 1
    if int(x[4:6]) < int(y[4:6]):
        return - 1
    if int(x[6:]) > int(y[6:]):
        return 1
    if int(x[6:]) < int(y[6:]):
        return - 1



def get_monthly_dates(start: str, end: str):
    dates = []
    date = start
    while cmp_dates(date, end) < 1:
        dates.append(date)
        date = increment_month(date)
    return dates

def get_yearly_dates(start: str, end: str):
    dates = []
    date = start
    while cmp_dates(date, end) < 1:
        dates.append(date)
        date = increment_year(date)
    return dates

def get_dates_interval_list(dates):
    intervals = []
    for start, end in zip(dates[:-1], dates[1:]):
        intervals.append((start, end))
    return intervals


def main():
    print(get_monthly_dates('20070000', '20200000'))

if __name__ == "__main__":
    sys.exit(main())
