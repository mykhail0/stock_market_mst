"""
    Część wspólna przetwarzania danych spółek z arkuszy do DataFrame
"""

import os
import sys
import pandas as pd

from stooq_archive_specific_parser_functions import preprocess_df


# Pobiera DataFrame z pliku `path` pewnej firmy.
get_df = lambda path: preprocess_df(pd.read_csv(path))


def merge_df(data):
    # data jest typu `list <DataFrame>`
    # Tworzy z takiej listy jeden DataFrame,
    # kolejne DataFrame dodaje jako nowe kolumny.
    return pd.concat(data, axis = 1)


def get_matrix(path: str):
    """
        Dostaje nazwę ścieżki, zwraca DataFrame z 
        wektorami spółek.

        Kolejne kolumny nazywają się jak skróty spółki,
        a każda kolumna jest wektorem spółki.
    """
    companies = []
    if not path.endswith('/'):
        path = path + '/'

    for companyData in os.listdir(path):
        companies.append(get_df(path + companyData))

    matrix = merge_df(companies)
    return matrix


def main(path: str):
    print(get_matrix(path))


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        exit("Usage: python script.py path/to/directory/with/sheets.cvs")

    sys.exit(main(args[0]))
