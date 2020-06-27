import sys
from graph_lib import bw_arr

from dates import *

from process_matrix import make_plot

def main(path: str):
    year_date_intervals = get_dates_interval_list(get_yearly_dates('20070000',
                          '20210000'))
    year_dates = make_dates_readable(year_date_intervals)


    month_date_intervals = get_dates_interval_list(get_monthly_dates('20190100',
                           '20200600'))
    month_dates = make_dates_readable(month_date_intervals)

    bw = bw_arr(path, year_date_intervals, 'KGH')
    make_plot(year_dates, bw, 'betweenness_for_KGH')


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        exit("Usage: python script.py path/to/Stooq/sheets")

    sys.exit(main(args[0]))
