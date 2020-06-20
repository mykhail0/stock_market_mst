"""
    Funkcje specyficzne do przetwarzania następującego typu danych:
        przetwarzanie pliku .txt z archiwum pobranego ze stooq.pl
        (tzn. filtrowanie niepotrzebnych danych,
         zmiana nazewnictwa kolumn/wierszy).
"""
import os
import sys
import pandas as pd



def preprocess_df(df):
    name = df.iloc[0]['<TICKER>']

    # usunięcie zbędnych danych
    # WEKTOR STANOWIĄ WARTOŚCI Z KOLUMNY <CLOSE>
    for f in ['<TICKER>', '<PER>', '<TIME>', '<OPEN>', \
              '<HIGH>', '<LOW>', '<VOL>', '<OPENINT>']:
        del df[f]

    df['<CLOSE>'] = df['<CLOSE>'].astype(float)

    # zamiana indeksów
    df = df.set_index('<DATE>')
    df.index.names = [None]

    # zmiana nazewnictwa
    df.rename(columns = {'<CLOSE>': name}, inplace = True)
    return df



def main():
    print("This module offers too specific functions")

if __name__ == "__main__":
    sys.exit(main())
