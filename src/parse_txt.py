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


def process_df(df):
    # usunięcie zbędnych danych
    name = df.iloc[0]['<TICKER>']
    for f in ['<TICKER>', '<PER>', '<TIME>', '<OPEN>', \
              '<HIGH>', '<LOW>', '<VOL>', '<OPENINT>']:
        del df[f]

    # obliczenie wektora spółki
    df['<CLOSE>'] = df['<CLOSE>'].astype(float)
    tmp = pd.Series(df['<CLOSE>'])
    df['<CLOSE>'] = df['<CLOSE>'].diff().div(tmp)

    # zamiana indeksów
    df = df.set_index('<DATE>')
    df.index.names = [None]

    # zmiana nazewnictwa
    df.rename(columns = {'<CLOSE>': name}, inplace = True)
    return df


get_df = lambda path: process_df(pd.read_csv(path))


def merge_df(data):
    return pd.concat(data, axis = 1)


def get_correlation_matrix(path):
    companies = []
    if not path.endswith('/'):
        path = path + '/'

    for companyData in os.listdir(path):
        companies.append(get_df(path + companyData))

    correlations = merge_df(companies).corr()
    return correlations


def main(path):
    print(get_correlation_matrix(path))

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        exit("Usage: python script.py path/to/directory/with/Stooq/sheets")

    sys.exit(main(args[0]))
