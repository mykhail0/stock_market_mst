"""
    Pobieramy ileś tam .csv z stooq.pl do jednego foldera.
    Skrypt tworzy macierz typu DataFrame ze współczynnikami
    korelacji pomiędzy spółkami.
    Kolejne kolumny nazywają się jak skróty spółki,
    a każda kolumna jest wektorem spółki.
    (Stopa zwrotu w dniu 't', wzór nr 3
    z proponowanych w pracie magisterskiej Sienkiewicza)
    
"""
import os
import sys
import pandas as pd
from graph_tool.all import *


def process_df(df, name):
    # usunięcie zbędnych danych
    for f in ['Otwarcie', 'Najwyzszy', 'Najnizszy', 'Wolumen']:
        del df[f]
    df['Zamkniecie'] = df['Zamkniecie'].astype(float)
    tmp = pd.Series(df['Zamkniecie'])

    # obliczenie wektora spółki
    value = df['Zamkniecie'].diff().div(tmp)

    # zamiana indeksów
    df = df.assign(Zamkniecie = value).set_index('Data')

    # zmiany wizualne w DataFrame
    df.rename(columns = {'Zamkniecie': name}, inplace=True)
    df.index.names = [None]
    return df


get_df = lambda path, name: process_df(pd.read_csv(path), name)


def merge_df(data):
    return pd.concat(data, axis = 1)


def get_correlations_matrix(path):
    companies = []
    if not path.endswith('/'):
        path = path + '/'

    for companyData in os.listdir(path):
        name = companyData
        if name.endswith('_d.csv'):
            name = name[:-6]
        companies.append(get_df(path + companyData, name))
    correlations = merge_df(companies).corr()
    return correlations


def main(path):
    print(get_correlations_matrix(path))

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        exit("Usage: python script.py path/to/directory/with/Stooq/sheets")

    sys.exit(main(args[0]))
