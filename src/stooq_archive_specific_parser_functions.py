"""
    Funkcje specyficzne do przetwarzania następującego typu danych:
        przetwarzanie pliku .txt z archiwum pobranego ze stooq.pl
        (tzn. filtrowanie niepotrzebnych danych,
         zmiana nazewnictwa kolumn/wierszy).

    TODO na razie też liczy wektory ale trzeba to zepchnąć na process_matrix
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

    # to najlepiej wyniesc do process matrix do funkcji calc_vectors()
    tmp = pd.Series(df['<CLOSE>'])
    df['<CLOSE>'] = df['<CLOSE>'].diff().div(tmp)

    # zamiana indeksów
    df = df.set_index('<DATE>')
    df.index.names = [None]

    # zmiana nazewnictwa
    df.rename(columns = {'<CLOSE>': name}, inplace = True)
    return df



def main():
    print("This module offers too specific functions")
    pass

if __name__ == "__main__":
    sys.exit(main())
